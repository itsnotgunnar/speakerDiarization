# speakerDiarization

This Python script contains a class `AudioProcessor` which is used for processing audio files. 

## Dependencies

You must setup a conda environment. Download Miniconda3 or Anaconda and run the following script:

```
conda env create -f environment.yml
conda activate myenv
source activate myenv
```

## Usage

Here's a simple example to get you started:

python

from AudioProcessor import AudioProcessor

### Initialize the processor

processor = AudioProcessor(sounds_id="some_id", file_path="path/to/audio/file")

### Run the main loop

processor.mainLoop()

## Methods

__init__(self, sounds_id, file_path)

Initializes the AudioProcessor object.
get_video_id(self, video_url)

Extracts the video ID from a given URL.
speaker_diarization(self)

Performs speaker diarization on the audio file.
millisec(self, timeStr)

Converts a time string to milliseconds.
primary_speaker(self)

Identifies the primary speaker in the audio.
chunk_primary(self)

Segments the audio based on the primary speaker.
transcribe_directory(self)

Transcribes all .wav files in a given directory.
audio_to_audioSeg(self, t1, t2)

Extracts an audio segment between t1 and t2.
mainLoop(self)

The main function that ties all the methods together.

## Environment Variables

The script uses the following environment variables:

- `OPENAI_API_KEY`: The API key for OpenAI.
- `HUG_USER1`: The API key for Hugging Face.

Make sure to set these environment variables before running the script.

## Contributing

Feel free to open issues or PRs if you find any problems or have suggestions for improvements.
