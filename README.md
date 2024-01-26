# AudioPhoneticsLab: Vowel Analysis and Detection

## Description
AudioPhoneticsLab is a repository dedicated to the analysis of vocal audio files. It focuses on extracting formant frequencies (F1 and F2) to identify specific vowels within an audio file. The repository contains two primary Python scripts: one for analyzing and setting parameters for each vowel based on given audio samples, and another for analyzing a `.wav` audio file to detect these vowels.

## Features
- **Vowel Parameter Analysis:** Analyzes specific audio files for each vowel (a, e, i, o, u) to determine the maximum and minimum frequencies of formants F1 and F2.
- **Vowel Detection in Audio:** Uses the analyzed vowel parameters to detect the presence of specific vowels in any given `.wav` audio file.

## How It Works
1. **Vowel Parameter Setting:** The script `scripts/audio_analytics/numeric_analytics.py` analyzes predefined audio samples for each vowel. It calculates and stores the max and min values of formants F1 and F2 in a JSON file (`results_max_min_frecuency_per_vocal.json`).
2. **Vowel Detection:** The script `scripts/wav_vowels_detect.py` uses the generated JSON file with vowel parameters to analyze a new audio file. It detects the start and end times of each vowel present in the audio.

## Usage
1. Run `set_vowel_parameters.py` with the audio samples of each vowel to generate the JSON file with vowel formant parameters.
2. Use `detect_vowels_in_audio.py` to analyze any `.wav` audio file for vowel detection. The results will be saved in `vowel_detections.json`.

## Requirements
- Python 3
- Parselmouth
- Numpy
- Matplotlib

## Contribution
Contributions to the project are welcome. Please ensure to follow the coding standards and add appropriate tests for new features.

## License
[Specify License]

## Contact
[Your Contact Information]
