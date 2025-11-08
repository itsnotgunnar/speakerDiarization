# Speaker Diarization

> A Python script for processing audio files, featuring speaker recognition and more.

---

## Features at a Glance

- **Speaker Diarization**: Identify who’s speaking and when.  
- **Primary Speaker Detection**: Find out who talks the most.  
- **Audio Segmentation**: Extract and manipulate audio segments.  
- **Batch Processing**: Transcribe entire directories of audio files.

---

## Dependencies

This repository uses a conda environment. Once you have **Miniconda** or **Anaconda** installed, run the following commands (replacing <MY_ENV> with the name of your environment):

```bash
conda env create -f environment.yml
conda activate <MY_ENV>
source activate <MY_ENV>
```

---

## Usage

A simple example to get you started:

```python
from AudioProcessor import AudioProcessor

# 1. Initialize the processor
processor = AudioProcessor(sounds_id="some_id", file_path="path/to/audio/file")

# 2. Run the main loop
processor.mainLoop()
```

---

## Class Methods Breakdown

Below is a rundown of the main methods in the `AudioProcessor` class:

1. **__init__(self, sounds_id, file_path)**  
   Initializes the AudioProcessor object.

2. **get_video_id(self, video_url)**  
   Extracts the video ID from a given URL.

3. **speaker_diarization(self)**  
   Performs speaker diarization on the audio file.

4. **millisec(self, timeStr)**  
   Converts a time string to milliseconds.

5. **primary_speaker(self)**  
   Identifies the primary speaker in the audio.

6. **chunk_primary(self)**  
   Segments the audio based on the primary speaker.

7. **transcribe_directory(self)**  
   Transcribes all .wav files in a given directory.

8. **audio_to_audioSeg(self, t1, t2)**  
   Extracts an audio segment between t1 and t2.

9. **mainLoop(self)**  
   Orchestrates all the methods, providing an end-to-end processing flow.

---

## Environment Variables

Be sure to set these environment variables before running the script:

- `OPENAI_API_KEY` – Your OpenAI API key.  
- `HUG_USER1` – Your Hugging Face API key.

---

## Contributing

Got ideas or found a bug? Feel free to open an issue or submit a PR. Contributions are always welcome!  
Let’s make this project even better, together. 

---
