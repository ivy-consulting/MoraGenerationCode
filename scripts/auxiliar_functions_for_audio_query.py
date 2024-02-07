from pydub import AudioSegment
import numpy as np
import aubio
import os
import json


def calculate_pitch(audio_path, symbols, sample_rate=24000):
    """
    Calculate the average pitch for each symbol in a given list.
    
    Parameters:
    - audio_path (str): Path to the audio file.
    - symbols (list): List of symbols with start and end times.
    - sample_rate (int): Sample rate for pitch analysis.
    
    Returns:
    - list: Updated list of symbols with pitch information added.
    """
    audio = AudioSegment.from_file(audio_path)
    pitch_detector = aubio.pitch("default", 2048, 512, sample_rate)
    pitch_detector.set_unit("Hz")
    pitch_detector.set_tolerance(0.8)

    for symbol in symbols:
        start_ms = int(symbol["start"] * 1000)
        end_ms = int(symbol["end"] * 1000)
        segment = audio[start_ms:end_ms]
        samples = np.array(segment.get_array_of_samples())

        # Convirtiendo las muestras a float32 necesario para Aubio
        samples_float = samples.astype(np.float32)
        # Aubio espera un array de una dimensión, por lo que es necesario aplanar el array si es estéreo
        if segment.channels == 2:
            samples_float = np.mean(samples_float.reshape((-1, 2)), axis=1)

        pitch_list = []

        # El buffer ya está en formato float, podemos pasar directamente a Aubio
        buffer_size = 512  # Adjust as needed
        hop_size = buffer_size // 2  # Typical overlap of 50%
        for i in range(0, len(samples_float) - buffer_size, hop_size):
            frame = samples_float[i:i+buffer_size]
            pitch = pitch_detector(frame)[0]
            if pitch > 0:  # Exclude 0 values which are unvoiced segments
                pitch_list.append(pitch)

        # Calculate average pitch for the segment
        if pitch_list:
            avg_pitch = sum(pitch_list) / len(pitch_list)
        else:
            avg_pitch = 0  # Consider how to handle segments without detectable pitch

        symbol["pitch"] = round(avg_pitch, 2)

    return symbols

def distribute_time_equally(start, end, text, decimals=4):
    """
    Distributes the time among the symbols of a word, excluding specific symbols.
    Symbols in 'filtered_text' at the start are grouped with the next symbol.
    Other symbols in 'filtered_text' are grouped with the preceding symbol.

    Parameters:
    - start (float): Start time.
    - end (float): End time.
    - text (str): The text to distribute time over.
    - decimals (int): Number of decimal places to round the time values.

    Returns:
    - list: A list of dictionaries, each containing the symbol (or symbol group) and its start and end times.
    """
    punctuation_symbols = ['ー', 'ッ', '゜', '゛', '?', '。', '、', '「', '」', '『', '』', '（', '）', '・', 'ゝ', 'ゞ', 'ヽ', 'ヾ']

    # Initialize variables
    grouped_symbols = []
    i = 0
    
    # Special case for the first symbol
    if text[0] in punctuation_symbols and len(text) > 1:
        grouped_symbols.append(text[0] + text[1])
        i = 2  # Skip the next symbol since it's already grouped
    
    # Group symbols, excluding specific ones as per the filtered list
    while i < len(text):
        current_symbol = text[i]
        next_symbol = text[i + 1] if i + 1 < len(text) else ""
        
        # Group current symbol with next if next symbol is in punctuation_symbols
        if next_symbol in punctuation_symbols:
            grouped_symbols.append(current_symbol + next_symbol)
            i += 2  # Skip the next symbol
        else:
            grouped_symbols.append(current_symbol)
            i += 1
    
    duration = end - start
    num_grouped_symbols = len(grouped_symbols)
    duration_per_group = duration / num_grouped_symbols
    
    symbols_times = []
    for i, symbol_group in enumerate(grouped_symbols):
        symbol_start = start + i * duration_per_group
        symbol_end = symbol_start + duration_per_group
        symbols_times.append({
            "text": symbol_group,
            "start": round(symbol_start, decimals),
            "end": round(symbol_end, decimals),
            "vowel_consonant_length ": round(symbol_end - symbol_start, decimals),
            "is_interrogative": "か" in symbol_group or "?" in symbol_group
        })
    
    return symbols_times

def add_consonant_vowel_info(symbols, mapping_file):
    """
    Adds consonant and vowel information to each symbol.
    """
    punctuation_symbols = ['ー', 'ッ', '゜', '゛', '?', '。', '、', '「', '」', '『', '』', '（', '）', '・', 'ゝ', 'ゞ', 'ヽ', 'ヾ']

    if not os.path.exists(mapping_file):
        print(f"Mapping file {mapping_file} does not exist. Adding null for consonant and vowel.")
        for symbol in symbols:
            symbol["consonant"] = None
            symbol["vowel"] = None
        return symbols

    with open(mapping_file, 'r', encoding='utf-8') as file:
        mapping = json.load(file)

    for symbol in symbols:
        symbol_without_punctuation = ''.join([char for char in symbol["text"] if char not in punctuation_symbols])
        char_info = mapping.get(symbol_without_punctuation.strip(), {})
        symbol["consonant"] = char_info.get("consonant", None)
        symbol["vowel"] = char_info.get("vowel", None)
    
    return symbols