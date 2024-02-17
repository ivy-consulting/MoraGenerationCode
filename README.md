# AudioPhoneticsLab

## Overview
AudioPhoneticsLab is a specialized repository focusing on processing audio files to transcribe speech and assigning timestamps to each phonetic symbol in the transcription. The primary function of this repository is to take an audio input, transcribe it using the `whisper-timestamped` model, and then distribute the duration of each transcribed word among its constituent symbols. This process results in a detailed mapping of when each symbol in the spoken language begins and ends in the audio.

## Features
- **Audio Transcription**: Utilizes `whisper-timestamped` to transcribe spoken words in an audio file.
- **Symbol-Level Timestamps**: Breaks down each word into its constituent symbols and assigns a start and end timestamp to each, offering a detailed view of the speech progression.

## Requirements
- Python 3.x
- whisper-timestamped
- Other dependencies as required by `whisper-timestamped`
- ffmpeg

## Installation
To set up the AudioPhoneticsLab environment, clone the repository and install the required packages:

```bash
git clone https://github.com/your-username/AudioPhoneticsLab.git
cd AudioPhoneticsLab
pip install whisper-timestamped
sudo apt update
sudo apt install ffmpeg
```

## Usage
The main script for processing audio files is located at `scripts/speech_symbol_timestamps.py` This script performs the following steps:

Loads a specified audio file.
Transcribes the audio to text using whisper-timestamped.
Distributes the duration of each word in the transcription among its constituent symbols.
Saves the results with detailed timestamps in a JSON file.
To run the script, navigate to the script's directory and execute it with Python:

```bash

python scripts/speech_symbol_timestamps.py
Output
The script outputs a JSON file named speech_symbol_timestamps.json, which contains the transcription of the audio file and the start and end timestamps for each symbol in the transcription. This file is structured to provide a clear and detailed view of the speech's progression at the symbol level.
```
## Contributions
Contributions to AudioPhoneticsLab are welcome. If you have an idea or improvement, feel free to fork the repository and submit a pull request.


## Acknowledgments
OpenAI's Whisper project for providing the base model for audio transcription.
The community of developers and researchers in the field of speech recognition and processing.