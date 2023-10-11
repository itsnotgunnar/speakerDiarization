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
from videos import Videos

class AudioProcessor:
    def __init__(self, sounds_id, file_path):
        self.sounds_id = sounds_id
        self.file_path = file_path
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=os.environ.get('HUG_USER1'))
        self.audio = None
        self.speaker = None
        self.lenAudio = None
        self.directory_name = f'./data/{self.sounds_id}'
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)

    # create environments.txt file for conda env

    def get_video_id(self, video_url):
        video_id = re.findall(r'(?<=v=)[\w-]+', video_url)
        if not video_id:
            video_id = re.findall(r'(?<=be/)[\w-]+', video_url)
        return video_id[0]

    def speaker_diarization(self):
        print("started speaker_diarization")
        TATE_FILE = {'uri': 'blabal', 'audio': f'./data/{self.sounds_id}.wav'} # TODO INCREMENT FILE
        dz = self.pipeline(TATE_FILE)
        howdy = dz
        lenAudio = len(dz) * 1000
        with open(f"diarization_{self.sounds_id}.txt", "w") as text_file:
            text_file.write(str(dz) + '\n')
            text_file.write(("-" * 30) + "\n")
            with open("tateDump.txt", "a") as dump:
                dump.write(str(dz) + "\n")
        print("finished speaker_diarization")
        return dz, lenAudio

    def millisec(self, timeStr):
        spl = timeStr.split(":")
        s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
        return s

    def primary_speaker(self): 
        dz = open(f'diarization_{self.sounds_id}.txt').read().splitlines()
        speaker_dict, speaker, speaker_clout, = {}, '', 0
        spacer = AudioSegment.silent(duration=2000)
        for i in range(len(dz) - 2):
            if dz[i][0] != '[':
                break
            line = dz[i]
            start, end =  tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=line))
            start = int(self.millisec(start))
            end = int(self.millisec(end))
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

    def chunk_primary(self):
        dz = open(f'diarization_{self.sounds_id}.txt').read().splitlines()
        print(self.speaker)
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
            start = int(self.millisec(start))
            end = int(self.millisec(end))
            chunk_length = (end - start) // 1000
            if line[0] == '-':
                return sounds, segments
            name = line[line.find('SPEAKER'):]
            if name == self.speaker and chunk_index > 0:
                chunk_index += 1
                audioChunk = self.audio[start:end]
                # sounds = spacer
                # segments.append(len(sounds))
                # sounds = sounds.append(audio[start:end], crossfade=0)
                audioChunk.export(f"{self.directory_name}/{sounds_id}p{chunk_index}-{chunk_length}secs.wav", format="wav")
        return (sounds, segments) # sounds getting wiped


    def chunk_1_secs(self):
        # made to train speech recognition, NOT USED
        directory_name = f'./recognition_dataset/audio_tate'
        dz = open('diarization.txt').read().splitlines()
        print(self.speaker)
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
            start = int(self.millisec(start))
            end = int(self.millisec(end))
            chunk_length = (end - start) // 1000
            if line[0] == '-':
                return sounds, segments
            name = line[line.find('SPEAKER'):]
            if name == self.speaker and chunk_index > 0:
                chunk_start = 0
                chunk_end = 1000
                for j in range(chunk_length):
                    audioChunk = self.audio[start:end]
                    audioChunk.export(f"{directory_name}/{chunk_index}.wav", format="wav")
                    chunk_start += 1000
                    chunk_end += 1000
                    chunk_index += 1
        
        # return (sounds, segments) 

    def transcribe_directory(self):
        model = whisper.load_model("base.en")
        # Loop through the files in the specified directory
        for file_name in os.listdir(self.directory_name):
            # Check if the file has a '.wav' extension
            if file_name.endswith('.wav'):
                # Get the full file path
                file_path = os.path.join(self.directory_name, file_name)

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

    def audio_to_audioSeg(self, t1, t2): # may need to increment index to keep segments
        a = AudioSegment.from_wav() # TODO INCREMENT FILE
        audioSegment = a[t1:t2]
        audioSegment.export("audio.wav", format="wav")
        # return audioSegment # commenting only to see whether this is currently used (5/1/23)

    def mainLoop(self): # TODO 'get_video_id(video_url)' not used, could not for dict key if not id or could use for file name and key 
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
        self.speaker_diarization() # does this run the function again (bc pipeline)
        speaker, lenAudio = self.primary_speaker()
        print(lenAudio)
        self.chunk_primary()
        # chunk_1_secs(audio, sounds_id, speaker)
        # transcribe_directory(directory_name)

if __name__ == "__main__":
    for sounds_id in range(32):
        processor = AudioProcessor(sounds_id, f'/home/gunna/.conda/envs/gpTate/tate_downloads/{sounds_id}.wav')
        processor.mainLoop()
    print("Finished transcription!")
