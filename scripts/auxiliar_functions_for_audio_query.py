import json
import os

import aubio
import numpy as np
from pydub import AudioSegment
import pykakasi 


def calculate_pitch(audio_path, symbols, sample_rate=24000):
    """
    Calculates the average pitch for each symbol in a provided list, using the specified audio file.
    
    This function processes an audio file to determine the pitch of individual symbols (e.g., phonemes, letters)
    within specified time intervals. It uses the Aubio library to analyze pitch values and updates each symbol
    with its average pitch.
    
    Parameters:
    - audio_path (str): The path to the audio file to be analyzed.
    - symbols (list): A list of dictionaries, each representing a symbol with 'start' and 'end' keys indicating
      the time interval for pitch analysis.
    - sample_rate (int): The sample rate to be used for pitch analysis. Defaults to 24000 Hz, which is adequate
      for most applications.
    
    Returns:
    - list: The input list of symbols, updated with a 'pitch' key for each symbol representing its average pitch
      in Hertz.
    """
    audio = AudioSegment.from_file(audio_path)  # Load the audio file using PyDub.
    pitch_detector = aubio.pitch("default", 2048, 512, sample_rate)  # Initialize the Aubio pitch detector.
    pitch_detector.set_unit("Hz")  # Set the unit of pitch detection to Hertz.
    pitch_detector.set_tolerance(0.8)  # Set the tolerance for pitch detection.

    for symbol in symbols:
        # Convert symbol start and end times from seconds to milliseconds.
        start_ms = int(symbol["start"] * 1000)
        end_ms = int(symbol["end"] * 1000)
        segment = audio[start_ms:end_ms]  # Extract the audio segment for the current symbol.
        samples = np.array(segment.get_array_of_samples())  # Get the raw audio samples as a NumPy array.

        # Convert samples to float32, as required by Aubio for pitch analysis.
        samples_float = samples.astype(np.float32)
        # If the audio segment is stereo, convert it to mono by averaging the two channels.
        if segment.channels == 2:
            samples_float = np.mean(samples_float.reshape((-1, 2)), axis=1)

        pitch_list = []  # Initialize a list to hold pitch values for the segment.

        # Analyze pitch for each frame within the segment.
        buffer_size = 512  # Define the buffer size for pitch analysis.
        hop_size = buffer_size // 2  # Define the hop size (50% overlap between frames).
        for i in range(0, len(samples_float) - buffer_size, hop_size):
            frame = samples_float[i:i+buffer_size]  # Extract the current frame.
            pitch = pitch_detector(frame)[0]  # Detect pitch for the current frame.
            if pitch > 0:  # Exclude frames with no detectable pitch.
                pitch_list.append(pitch)

        # Calculate the average pitch for the segment, or set to 0 if no pitch was detected.
        avg_pitch = sum(pitch_list) / len(pitch_list) if pitch_list else 0

        # Update the current symbol with its average pitch.
        symbol["pitch"] = round(avg_pitch/1000, 7) # The final units are kHz.

    return symbols  # Return the updated list of symbols with pitch information.


def distribute_time_equally(start, end, text, decimals=4):
    """
    This function distributes the time evenly among the symbols of a given text. It specifically handles
    Japanese punctuation symbols by either grouping them with the preceding or following symbol to ensure
    that time allocation reflects natural speech patterns. Additionally, it checks for interrogative symbols
    to mark symbols as part of a question.

    Parameters:
    - start (float): The start time of the audio segment corresponding to the text.
    - end (float): The end time of the audio segment corresponding to the text.
    - text (str): The text content to be analyzed and distributed across the time segment.
    - decimals (int): The number of decimal places to which time values should be rounded.

    Returns:
    - list: A list of dictionaries, each containing details about the symbol, its start and end time within
      the audio segment, its duration, and whether it is part of an interrogative segment (question).
    """
    # List of Japanese punctuation symbols that may affect how time is distributed among symbols.
    punctuation_symbols = ['ー', 'ッ', '゜', '゛', '?', '。', '、', '「', '」', '『', '』', '（', '）', '・', 'ゝ', 'ゞ', 'ヽ', 'ヾ']

    # Initialize the list to store the processed symbols and their time allocations.
    grouped_symbols = []
    i = 0  # Index to keep track of the current position in the text.
    
    # Handle the case where the first symbol is a punctuation that should be grouped with the following symbol.
    if text[0] in punctuation_symbols and len(text) > 1:
        grouped_symbols.append(text[0] + text[1])  # Group the first symbol with the next one.
        i = 2  # Move the index past the grouped symbols.
    
    # Iterate through the text to group symbols as needed.
    while i < len(text):
        current_symbol = text[i]  # The current symbol being processed.
        # Determine the next symbol if it exists, otherwise set it to an empty string.
        next_symbol = text[i + 1] if i + 1 < len(text) else ""
        
        # Check if the current symbol or the next symbol is a punctuation symbol.
        if next_symbol in punctuation_symbols:
            grouped_symbols.append(current_symbol + next_symbol)  # Group them together.
            i += 2  # Skip the next symbol as it has been grouped with the current one.
        else:
            grouped_symbols.append(current_symbol)  # No grouping needed; add the symbol as is.
            i += 1  # Move to the next symbol.
    
    # Calculate the total duration of the segment and the duration per grouped symbol.
    duration = end - start
    num_grouped_symbols = len(grouped_symbols)
    duration_per_group = duration / num_grouped_symbols  # Evenly distribute time across symbols.
    
    # Create a list to store the timing and details for each symbol or symbol group.
    symbols_times = []
    for i, symbol_group in enumerate(grouped_symbols):
        # Calculate the start and end times for each symbol or group.
        symbol_start = start + i * duration_per_group
        symbol_end = symbol_start + duration_per_group
        # Append the symbol details, including whether it's part of an interrogative segment.
        symbols_times.append({
            "text": symbol_group,
            "start": round(symbol_start, decimals),
            "end": round(symbol_end, decimals),
            "vowel_consonant_length": round(symbol_end - symbol_start, decimals)
        })
    
    return symbols_times  # Return the list of symbols with their allocated times and additional details.


def add_consonant_vowel_info(symbols, mapping_file):
    """
    Enriches each symbol in the provided list with consonant and vowel information based on a mapping file.
    
    This function reads a mapping from the given JSON file, which associates each symbol with its corresponding
    consonant and vowel components. It then updates each symbol dictionary in the list with this phonetic information.
    If a symbol is punctuation or not found in the mapping, its consonant and vowel values are set to None.
    
    Parameters:
    - symbols (list): A list of dictionaries, each representing a symbol with 'text', and potentially other keys.
    - mapping_file (str): Path to the JSON file containing the consonant and vowel mapping for symbols.
    
    Returns:
    - list: The same list of symbols, but updated to include 'consonant' and 'vowel' keys for each symbol.
    """
    # Define punctuation symbols that do not have consonant/vowel information.
    punctuation_symbols = ['ー', 'ッ', '゜', '゛', '?', '。', '、', '「', '」', '『', '』', '（', '）', '・', 'ゝ', 'ゞ', 'ヽ', 'ヾ']

    # Check if the mapping file exists, warn and proceed with null values if not.
    if not os.path.exists(mapping_file):
        print(f"Mapping file {mapping_file} does not exist. Adding null for consonant and vowel.")
        for symbol in symbols:
            symbol["consonant"] = None
            symbol["vowel"] = None
        return symbols  # Return the symbols list early if the mapping file is missing.

    # Load the mapping from the JSON file.
    with open(mapping_file, 'r', encoding='utf-8') as file:
        mapping = json.load(file)

    # Iterate over each symbol to add consonant and vowel information.
    for symbol in symbols:
        # Remove any punctuation from the symbol's text before looking it up in the mapping.
        symbol_without_punctuation = ''.join([char for char in symbol["text"] if char not in punctuation_symbols])
        # Fetch the symbol's phonetic information from the mapping, defaulting to an empty dict.
        char_info = mapping.get(symbol_without_punctuation.strip(), {})
        # Update the symbol with its consonant and vowel information, defaulting to None if not found.
        symbol["consonant"] = char_info.get("consonant", None)
        symbol["vowel"] = char_info.get("vowel", None)
    
    return symbols  # Return the updated list of symbols with added phonetic information.


def time_for_vowels_and_consonants(symbols):
    """
    Calculate and assign duration times to vowels and consonants within a list of symbolic representations.

    This function iterates over a list of symbol dictionaries, each representing a linguistic or phonetic
    symbol with associated metadata. It calculates the duration times for vowels and consonants based on
    predefined time allocation rules: each vowel is allocated four times the base duration unit, whereas
    each consonant is allocated one base duration unit. The function updates each symbol dictionary to
    include this calculated duration time for both vowels and consonants.

    Parameters:
    - symbols (list of dict): Each dictionary in the list should include the following keys:
        - 'text' (str): The textual representation of the symbol.
        - 'vowel_consonant_length' (float): The total duration allocated for both vowels and consonants.
        - 'vowel' (str or None): A string of vowels present in the symbol, or None if no vowels.
        - 'consonant' (str or None): A string of consonants present in the symbol, or None if no consonants.

    Returns:
    - list of dict: The input list, with each symbol dictionary updated to include two additional keys:
        - 'vowel_length' (float or None): The calculated duration for vowels, rounded to 4 decimal places;
          None if the symbol contains no vowels.
        - 'consonant_length' (float or None): The calculated duration for consonants, rounded to 4 decimal
          places; None if the symbol contains no consonants.
    """
    for symbol in symbols:
        # Identify the presence and count of vowels and consonants in the current symbol.
        vowels = symbol.get('vowel')
        consonants = symbol.get('consonant')
        len_vowels = len(vowels) if vowels else 0
        len_consonants = len(consonants) if consonants else 0

        # Compute the base time unit by dividing the total time by the weighted sum of vowels and consonants.
        total_time = symbol['vowel_consonant_length']
        if len_vowels or len_consonants:
            fraction_time = total_time / (len_vowels * 4 + len_consonants)
        else:
            fraction_time = 0  # Avoid division by zero when there are no vowels or consonants.

        # Calculate the total time dedicated to vowels and consonants based on their counts.
        time_vowels = fraction_time * 4 * len_vowels
        time_consonants = fraction_time * len_consonants
        
        # Update the symbol dictionary with calculated times, rounding to 4 decimal places.
        symbol['vowel_length'] = total_time if len_vowels > 0 else None
        symbol['consonant_length'] = round(time_consonants, 4) if len_consonants > 0 else None

    return symbols

# Translate the kanji  into hiragana

def text_to_kanji(text):
    """
    Detects the language of the input text and converts it to Kanji if it is Japanese.

    Parameters:
    - text (str): The text to analyze and possibly convert.

    Returns:
    - str: The original text if it's not Japanese, or the converted text in Kanji if it is Japanese.
    """
    
    kakasi = pykakasi.kakasi()

    # Set the conversion mode to convert to Kanji
    kakasi.setMode('H', 'K')  # Convert Hiragana to Kanji
    kakasi.setMode('K', 'K')  # Keep Katakana as Katakana
    kakasi.setMode('J', 'K')  # Convert Japanese (Kanji and Hiragana) to Kanji

    # Create a converter
    converter = kakasi.getConverter()

    # Convert the input text to Kanji
    kanji_text = converter.do(text)
    
    return kanji_text
    


def calculate_total_vowel_and_pause_time(audio_query): 
    """ 
    Calcula el tiempo total de las vocales y las pausas (pause mora) en el JSON proporcionado. 

    Parameters: 
    - audio_query (dict): Un diccionario que representa el JSON con la transcripción y detalles fonéticos. 

    Returns: 
    - float: El tiempo total en segundos de las vocales y las pausas no nulas. 
    """ 
    total_time = 0.0 

    for phrase in audio_query['accent_phrases']: 
        for mora in phrase['moras']: 
        # Sum the duration of the vowels        
            total_time += mora['vowel_consonant_length']
        if phrase['pause_mora'] is not None:
            # Sum the duration of the pause
            total_time += phrase['pause_mora']['vowel_length']
            if phrase['pause_mora']['consonant_length'] is not None:
                total_time += phrase['pause_mora']['consonant_length']  
    # Sum the duration of the final pause
    total_time += audio_query['final_pause'] if audio_query['final_pause'] is not None else 0
    return total_time 

def number_of_vowels_and_pauses(audio_query): 
    """
    Returns the number of vowels and pauses in the audio query.

    Parameters:
    - audio_query (dict): A dictionary representing the JSON with the transcription and phonetic details.

    Returns:
    - int: The number of vowels and pauses in the audio query.

    """
    number = 0 

    for phrase in audio_query['accent_phrases']: 
        for mora in phrase['moras']: 
            # Sum the number of vowels        
            number += len(mora)
        if phrase['pause_mora'] is not None:
            # Sum the number of pauses
            number += 1 
        if phrase['pause_mora'] is not None:
            # Sum the number of pauses for consonants if they are not None
            number += 1
            if phrase['pause_mora']['consonant_length'] is not None:
                number += 1  
    # Sum the number of the final pause
    if audio_query['final_pause'] is not None:
            number += 1
    return number 

def get_audio_duration(file_path): 
    """ 
    Returns the duration of an audio file in seconds. 

    Parameters: 
    - file_path (str): Path to the audio file. 

    Returns: 
    - float: Duration of the audio file in seconds. 
    """ 
    # Load the audio file using PyDub.
    audio = AudioSegment.from_file(file_path) 
    duration_seconds = len(audio) / 1000.0 # AudioSegment.length is in milliseconds 
    return duration_seconds 

def distribute_time_error_in_all_vowels_and_pauses(audio_query, audio_path):
    """
    Distribute the error in the total time of the audio query in all the vowels and pauses.

    Parameters:
    - audio_query (dict): A dictionary representing the JSON with the transcription and phonetic details.
    - audio_path (str): The path to the audio file.

    Returns:
    - dict: The input audio query
    """
    # Total time of vowels and pauses
    total_duration = calculate_total_vowel_and_pause_time(audio_query)

    # Total time of the audio
    audio_duration = get_audio_duration(audio_path)

    # Calculate the error
    error = audio_duration - total_duration

    # Number of vowels and pauses
    vowels_and_pauses = number_of_vowels_and_pauses(audio_query)

    # Distribute the error in all the vowels and pauses
    error_per_vowel_or_pause = error / vowels_and_pauses

    print("Error per vowel or pause:", error_per_vowel_or_pause)

    # Distribute the error in all the vowels and pauses
    for phrase in audio_query['accent_phrases']:
        for mora in phrase['moras']:
            mora['vowel_consonant_length'] = mora['vowel_consonant_length'] + error_per_vowel_or_pause if mora['vowel_consonant_length'] is not None else None
            mora['vowel_length'] = mora['vowel_length'] + error_per_vowel_or_pause if mora['vowel_length'] is not None else None

        if phrase['pause_mora'] is not None:
            phrase['pause_mora']['vowel_length'] = phrase['pause_mora']['vowel_length'] + error_per_vowel_or_pause
            if phrase['pause_mora']['consonant_length'] is not None:
                phrase['pause_mora']['consonant_length'] = phrase['pause_mora']['consonant_length'] + error_per_vowel_or_pause
    return audio_query

# Example usage 
if __name__ == "__main__": 
    original_text = "私は日本語を勉強しています。" 
    hiragana_text = text_to_hiragana(original_text) 
    print("Original text:", original_text) 
    print("Converted to Hiragana:", hiragana_text) 



if __name__ == "__main__":
    print(time_for_vowels_and_consonants(
        [
                {
                    "text": "ま",
                    "start": 1.6,
                    "end": 1.7067,
                    "vowel_consonant_length": 0.1067,
                    "consonant": "m",
                    "vowel": "a",
                    "pitch": 80.72
                },
                {
                    "text": "し",
                    "start": 1.7067,
                    "end": 1.8133,
                    "vowel_consonant_length": 0.1067,
                    "consonant": "sh",
                    "vowel": "i",
                    "pitch": 2862.93
                },
                {
                    "text": "た。",
                    "start": 1.8133,
                    "end": 1.92,
                    "vowel_consonant_length": 0.1067,
                    "consonant": "t",
                    "vowel": "a",
                    "pitch": 2266.33
                }
            ]))