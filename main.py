from pydub import AudioSegment
from pyannote.audio import Pipeline
from huggingface_hub import HfApi
import openai
import whisper
import logging
import string
import sys
import os
import re

class AudioProcessor:
    def __init__(self, sounds_id, file_path):
        self.sounds_id = sounds_id
        self.file_path = file_path
        self.pipeline = None
        self.audio = None
        self.speaker = None
        self.lenAudio = None
        self.directory_name = f'./data/{self.sounds_id}'
        self.init_pipeline()

    # create environments.txt file for conda env

    videos = {
        "girl-interview": "https://www.youtube.com/watch?v=HZ6FhDfa9UY",
        "destroyed-woman": "https://www.youtube.com/watch?v=DgRV3F_7BdQ",
        "funny-takes": "https://www.youtube.com/watch?v=DgRV3F_7BdQ",
        "how-to-rich": "https://www.youtube.com/watch?v=U5ylEzE9ktU",
        "destroys-feminist":"https://www.youtube.com/watch?v=AzKH0DCNowQ",
        "sexist": "https://www.youtube.com/watch?v=gexkQ8Y2G80",
        "best-podcast-moments": "https://www.youtube.com/watch?v=GOWFsme5u9E",
        "motivation": "https://www.youtube.com/watch?v=BX1WpL2VlhM",
        "quotes": "https://www.youtube.com/watch?v=lh4_41qpKUk",
        "top-lessons":"https://www.youtube.com/watch?v=EJcRcj5vBj8",
        "advice": "https://www.youtube.com/watch?v=3mBhMdthw-A",
        "women-cheat": "https://www.youtube.com/watch?v=aaXVVgOIpJM",
        "tiktok": "https://www.youtube.com/watch?v=TM7PWLBoh_o",
        "funniest":  "https://www.youtube.com/watch?v=yvRB0inZdWE",
        "toxic": "https://www.youtube.com/watch?v=G_D4r-24bgQ",
        "reinvent": "https://www.youtube.com/watch?v=kQCTfEphctc",
        "podcast-2": "https://www.youtube.com/watch?v=M3vw7-COfGA",
        "coldest": "https://www.youtube.com/watch?v=nbwHftL2-98",
        "piers-morgan": "https://www.youtube.com/watch?v=c1Whpnq1dAY",
        "top-g": "https://www.youtube.com/watch?v=6VFn-1oJqlk",
        "spitting-facts": "https://www.youtube.com/watch?v=-Ol2qiB9tdY",
        "most-savage": "https://www.youtube.com/watch?v=RatbWBeA6Fk",
        "brokies": "https://www.youtube.com/watch?v=IwPKg2kLkrg",
        "coldest-p2": "https://www.youtube.com/watch?v=gpRYrV_YMps",
        "islamic-faith": "https://www.youtube.com/watch?v=YzL_cRdba5k",
        "male-advice": "https://www.youtube.com/watch?v=Gp2PwNcj2x4",
        "inferior":"https://www.youtube.com/watch?v=U5ylEzE9ktU",
        "speeches": "https://www.youtube.com/watch?v=Uw37yw1ZuEI",
        "trolls-feminist": "https://www.youtube.com/watch?v=d4kAPWBH3e8",
        "why-muslim": "https://www.youtube.com/watch?v=vnTiTg0Ouhs",
        "weak-men": "https://www.youtube.com/watch?v=HtoxRMxb7yE",
        "long-patrick": "https://www.youtube.com/watch?v=ZfuSRR1jf1o"
    }

    def get_video_id(video_url):
        video_id = re.findall(r'(?<=v=)[\w-]+', video_url)
        if not video_id:
            video_id = re.findall(r'(?<=be/)[\w-]+', video_url)
        return video_id[0]

    def speaker_diarization(sounds_id,pipeline):
        print("started speaker_diarization")
        TATE_FILE = {'uri': 'blabal', 'audio': f'./data/{sounds_id}.wav'} # TODO INCREMENT FILE
        dz = pipeline(TATE_FILE)
        howdy = dz
        lenAudio = len(dz) * 1000
        with open(f"diarization_{sounds_id}.txt", "w") as text_file:
            text_file.write(str(dz) + '\n')
            text_file.write(("-" * 30) + "\n")
            with open("tateDump.txt", "a") as dump:
                dump.write(str(dz) + "\n")
        print("finished speaker_diarization")
        return dz, lenAudio

    def millisec(timeStr):
        spl = timeStr.split(":")
        s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
        return s

    def primary_speaker(sounds_id): 
        dz = open(f'diarization_{sounds_id}.txt').read().splitlines()
        speaker_dict, speaker, speaker_clout, = {}, '', 0
        spacer = AudioSegment.silent(duration=2000)
        for i in range(len(dz) - 2):
            if dz[i][0] != '[':
                break
            line = dz[i]
            start, end =  tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=line))
            start = int(millisec(start))
            end = int(millisec(end))
            first_letter = re.search("[a-zA-z]", line)
            name = line[line.find('SPEAKER'):]
            if name not in speaker_dict.keys():
                speaker_dict[name] = 0
            speaker_dict[name] += end - start
        print(speaker_dict)
        for key, value in speaker_dict.items():
            if speaker_clout == 0 or value > speaker_clout:
                speaker = key
                speaker_clout = value
        speaker = speaker[re.search("[a-zA-Z]", speaker).start():]
        return speaker, speaker_dict[speaker]

    def chunk_primary(audio, sounds_id, speaker, directory_name):
        dz = open(f'diarization_{sounds_id}.txt').read().splitlines()
        print(speaker)
        spacer = AudioSegment.silent(duration=10)
        sounds = spacer
        segments = []
        chunk_index = 0
        for i in range(len(dz) - 2):
            if dz[i][0] != '[':
                print(dz[i])
                break
            line = dz[i]
            start, end =  tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=line))
            start = int(millisec(start))
            end = int(millisec(end))
            chunk_length = (end - start) // 1000
            if line[0] == '-':
                return sounds, segments
            name = line[line.find('SPEAKER'):]
            if name == speaker and chunk_index > 0:
                chunk_index += 1
                audioChunk = audio[start:end]
                # sounds = spacer
                # segments.append(len(sounds))
                # sounds = sounds.append(audio[start:end], crossfade=0)
                audioChunk.export(f"{directory_name}/{sounds_id}p{chunk_index}-{chunk_length}secs.wav", format="wav")
        return (sounds, segments) # sounds getting wiped


    def chunk_1_secs(audio, sounds_id, speaker): # made to train speech recognition 
        directory_name = f'./recognition_dataset/audio_tate'
        dz = open('diarization.txt').read().splitlines()
        print(speaker)
        spacer = AudioSegment.silent(duration=0)
        sounds = spacer
        segments = []
        chunk_index = 0
        for i in range(len(dz) - 2):
            if dz[i][0] != '[':
                print(dz[i])
                break
            line = dz[i]
            start, end =  tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=line))
            start = int(millisec(start))
            end = int(millisec(end))
            chunk_length = (end - start) // 1000
            if line[0] == '-':
                return sounds, segments
            name = line[line.find('SPEAKER'):]
            if name == speaker and chunk_index > 0:
                chunk_start = 0
                chunk_end = 1000
                for j in range(chunk_length):
                    audioChunk = audio[start:end]
                    audioChunk.export(f"{directory_name}/{chunk_index}.wav", format="wav")
                    chunk_start += 1000
                    chunk_end += 1000
                    chunk_index += 1
        
        # return (sounds, segments) 

    def transcribe_directory(directory_name):
        model = whisper.load_model("base.en")
        # Loop through the files in the specified directory
        for file_name in os.listdir(directory_name):
            # Check if the file has a '.wav' extension
            if file_name.endswith('.wav'):
                # Get the full file path
                file_path = os.path.join(directory_name, file_name)

                # Load and transcribe the audio segment using Whisper
                whisper_audio = open(file=file_path)
                transcript = model.transcribe(
                    audio=file_path,
                    verbose=True,
                    initial_prompt="Be assertive. Be a man. Join me, and leave the matrix. Grow up! Just buy a Bugatti, make dollas, and get beautiful models as wives. Skeeter-rom-bomp the haters. You wanna be me. Hustlers University is for champions."
                )

                # Save the transcription to a text file
                with open(f"{os.path.splitext(file_path)[0]}.txt", "a") as f:
                    f.write(str(transcript))

    def audio_to_audioSeg(t1, t2): # may need to increment index to keep segments
        a = AudioSegment.from_wav() # TODO INCREMENT FILE
        audioSegment = a[t1:t2]
        audioSegment.export("audio.wav", format="wav")
        # return audioSegment # commenting only to see whether this is currently used (5/1/23)

    def mainLoop(sounds_id, file): # TODO 'get_video_id(video_url)' not used, could not for dict key if not id or could use for file name and key 
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        key = os.environ.get('HUG_USER1')
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=key)               
        print(sounds_id)
        t1, t2 = 0, 600000 # 10 minutes segments default / handle in audio_to_segment
        status = True
        directory_name = f'./data/{sounds_id}'
        if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        audio = AudioSegment.from_wav(f'./data/downloads/{sounds_id}.wav')
        audio.export(f"tate_audios/audio_{sounds_id}", "wav")
        speaker_diarization(sounds_id, pipeline) # does this run the function again (bc pipeline)
        speaker, lenAudio = primary_speaker(sounds_id)
        print(lenAudio)
        chunk_primary(audio, sounds_id, speaker, directory_name)
        # chunk_1_secs(audio, sounds_id, speaker)
        # transcribe_directory(directory_name)

if __name__ == "__main__":
    for sounds_id in range(32):
        processor = AudioProcessor(sounds_id, f'/home/gunna/.conda/envs/gpTate/tate_downloads/{sounds_id}.wav')
        processor.mainLoop()
    print("Finished transcription!")
