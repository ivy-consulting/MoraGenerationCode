from pydub import AudioSegment 

def get_audio_duration(file_path): 
    """ 
    Returns the duration of an audio file in seconds. 

    Parameters: 
    - file_path (str): Path to the audio file. 

    Returns: 
    - float: Duration of the audio file in seconds. 
    """ 
    audio = AudioSegment.from_file(file_path) 
    duration_seconds = len(audio) / 1000.0 # AudioSegment.length is in milliseconds 
    return duration_seconds 

# Example usage 
file_path = 'test_audios/001-sibutomo (1).mp3' # Replace with your actual file path 
duration = get_audio_duration(file_path) 
print(f"The duration of the audio file is {duration} seconds.") 

import json 

data = json.load(open('speech_symbol_timestamps.json'))

def calculate_total_vowel_and_pause_time(audio_query): 
    """ 
    Calcula el tiempo total de las vocales y las pausas (pause mora) en el JSON proporcionado. 

    Parameters: 
    - data (dict): Un diccionario que representa el JSON con la transcripción y detalles fonéticos. 

    Returns: 
    - float: El tiempo total en segundos de las vocales y las pausas no nulas. 
    """ 
    total_time = 0.0 

    for phrase in audio_query['accent_phrases']: 
        for mora in phrase['moras']: 
        # Sumar la duración de las vocales         
            total_time += mora['vowel_consonant_length']
        if phrase['pause_mora'] is not None:
            total_time += phrase['pause_mora']['vowel_length']
            if phrase['pause_mora']['consonant_length'] is not None:
                total_time += phrase['pause_mora']['consonant_length']  
    total_time += audio_query['final_pause'] if audio_query['final_pause'] is not None else 0

    return total_time 

# Llamar a la función y pasarle el JSON 
total_duration = calculate_total_vowel_and_pause_time(data) 
print(f"Total vowel and pause time: {total_duration} seconds")