import parselmouth
import numpy as np
import json

# Load the formant ranges for vowels from the JSON file
with open('results/results_max_min_frecuency_per_vocal.json', 'r') as file:
    vowel_ranges = json.load(file)

# Load the audio file for analysis
audio_path = "test_audios/u.wav"
snd = parselmouth.Sound(audio_path)

# Extract F1 and F2 from the audio
formants = snd.to_formant_burg()
duration = snd.get_total_duration()
times = np.linspace(0, duration, int(duration * 1000))  # Assuming 1000 points per second

# Vowel detection
detections = {}
for time in times:
    f1 = formants.get_value_at_time(1, time)
    f2 = formants.get_value_at_time(2, time)
    
    for vowel, ranges in vowel_ranges.items():
        if ranges['F1_min'] <= f1 <= ranges['F1_max'] and ranges['F2_min'] <= f2 <= ranges['F2_max']:
            if vowel not in detections:
                detections[vowel] = {'start': time, 'end': None}
            elif 'start' in detections[vowel] and not detections[vowel]['end']:
                detections[vowel]['end'] = time

# Save the detections in a JSON file
with open('vowel_detections.json', 'w') as fp:
    json.dump(detections, fp, indent=4)

print("Analysis completed and saved in 'vowel_detections.json'")
