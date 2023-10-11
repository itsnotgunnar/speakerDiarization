# speakerDiarization

This Python script contains a class `AudioProcessor` which is used for processing audio files. The class uses several libraries including `pydub`, `pyannote.audio`, `huggingface_hub`, `openai`, `whisper`, `logging`, `string`, `sys`, `os`, `re`, and `videos`.

## Dependencies

To run this script, you need to install the following Python libraries:

- pydub
- pyannote.audio
- huggingface_hub
- openai
- whisper
- logging
- string
- sys
- os
- re

You can install these libraries using pip:

```
pip install pydub pyannote.audio huggingface_hub openai whisper logging string sys os re
```

## Usage

The `AudioProcessor` class is initialized with a `sounds_id` and a `file_path`. The `sounds_id` is used to identify the audio file and the `file_path` is the location of the audio file.

The class contains several methods for processing the audio file:

- `get_video_id(video_url)`: Extracts the video ID from a YouTube URL.
- `speaker_diarization(sounds_id,pipeline)`: Performs speaker diarization on the audio file.
- `millisec(timeStr)`: Converts a time string to milliseconds.
- `primary_speaker(sounds_id)`: Identifies the primary speaker in the audio file.
- `chunk_primary(audio, sounds_id, speaker, directory_name)`: Splits the audio file into chunks based on the primary speaker.
- `chunk_1_secs(audio, sounds_id, speaker)`: Splits the audio file into 1 second chunks.
- `transcribe_directory(directory_name)`: Transcribes all audio files in a directory.
- `audio_to_audioSeg(t1, t2)`: Converts a segment of the audio file to an `AudioSegment`.
- `mainLoop(sounds_id, file)`: The main method for processing the audio file.

To use the `AudioProcessor` class, create an instance of the class and call the `mainLoop` method:

```python
processor = AudioProcessor(sounds_id, file_path)
processor.mainLoop()
```

## Environment Variables

The script uses the following environment variables:

- `OPENAI_API_KEY`: The API key for OpenAI.
- `HUG_USER1`: The API key for Hugging Face.

Make sure to set these environment variables before running the script.
