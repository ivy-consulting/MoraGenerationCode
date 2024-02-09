# AudioPhoneticsLab

## Overview
AudioPhoneticsLab is a specialized repository focusing on the transcription of audio files into text and enriching each transcribed word with detailed phonetic information. It takes an audio input, transcribes it using the `whisper-timestamped` model, distributes the duration of each transcribed word among its constituent symbols, calculates the pitch for each symbol, and identifies if the word forms a question. This results in a detailed mapping of when each symbol in the spoken language begins and ends in the audio, offering a clear and detailed view of speech progression.

## Features
- **Audio Transcription with Detailed Phonetic Information**: Utilizes the `whisper-timestamped` model to transcribe spoken words in an audio file and enriches the transcription with consonants and vowels information.
- **Symbol-Level Timestamps and Pitch Analysis**: Assigns a start and end timestamp to each symbol, along with the pitch, providing an in-depth analysis of the speech.
- **Interrogative Detection**: Identifies whether the transcribed words form a question, enhancing the understanding of speech's intent.
- **Customizable Output**: Offers options to save the transcription and analysis results into a JSON file, allowing for easy integration with other applications.

## Requirements
- Python 3.x
- Libraries in requirements.txt

## Installation
To set up the AudioPhoneticsLab environment, follow these steps:

```bash
git clone https://github.com/your-username/AudioPhoneticsLab.git
cd AudioPhoneticsLab
pip install -r requirements.txt
```

## Usage
To process an audio file, use the speech_symbol_timestamps.py script located in the scripts directory. This script will:

- Load the specified audio file.
- Transcribe the audio using the whisper-timestamped model.
- Distribute the duration of each word among its symbols.
- Add consonant and vowel information and calculate the pitch for each symbol.
- Save the results in a JSON file.
- Execute the script with the following command:

`python scripts/speech_symbol_timestamps.py`

## Output
The script outputs a JSON file named speech_symbol_timestamps.json, containing the transcription and detailed analysis of the audio file. This includes start and end timestamps for each symbol, pitch values, and whether each word is interrogative, structured to provide a comprehensive overview of speech progression.

## Contributions
Contributions to AudioPhoneticsLab are welcome. If you have an idea or improvement, feel free to fork the repository and submit a pull request.


## Acknowledgments
OpenAI's Whisper project for providing the base model for audio transcription.
The community of developers and researchers in the field of speech recognition and processing.