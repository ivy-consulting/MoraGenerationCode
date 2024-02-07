import whisper_timestamped
import json
import os

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
    filtered_text = ['ー', 'ッ', '゜', '゛', '?', '。', '、', '「', '」', '『', '』', '（', '）', '・', 'ゝ', 'ゞ', 'ヽ', 'ヾ']
    
    # Initialize variables
    grouped_symbols = []
    i = 0
    
    # Special case for the first symbol
    if text[0] in filtered_text and len(text) > 1:
        grouped_symbols.append(text[0] + text[1])
        i = 2  # Skip the next symbol since it's already grouped
    
    # Group symbols, excluding specific ones as per the filtered list
    while i < len(text):
        current_symbol = text[i]
        next_symbol = text[i + 1] if i + 1 < len(text) else ""
        
        # Group current symbol with next if next symbol is in filtered_text
        if next_symbol in filtered_text:
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
            "symbol": symbol_group,
            "start": round(symbol_start, decimals),
            "end": round(symbol_end, decimals),
            "vowel_consonant_length ": round(symbol_end - symbol_start, decimals)
        })
    
    return symbols_times

def add_consonant_vowel_info(symbols, mapping_file):
    """
    Adds consonant and vowel information to each symbol.
    """
    if not os.path.exists(mapping_file):
        print(f"Mapping file {mapping_file} does not exist. Adding null for consonant and vowel.")
        for symbol in symbols:
            symbol["consonant"] = None
            symbol["vowel"] = None
        return symbols

    with open(mapping_file, 'r', encoding='utf-8') as file:
        mapping = json.load(file)

    for symbol in symbols:
        char_info = mapping.get(symbol["symbol"], {})
        symbol["consonant"] = char_info.get("consonant", None)
        symbol["vowel"] = char_info.get("vowel", None)
    
    return symbols

def audio_query_json(audio_path, save_to_file=False, json_output_path="speech_symbol_timestamps.json", mapping_file="files/mapping.json"):
    """
    Transcribes an audio file and adds consonant and vowel information to each symbol.
    """
    model = whisper_timestamped.load_model("base", device="cpu")
    result = whisper_timestamped.transcribe(model, audio_path, language="ja")
    print(result)
    print("Complete transcription:", result["text"])

    data_to_save = {
        "transcription": result["text"],
        "symbols": []
    }

    for segment in result["segments"]:
        for word in segment.get("words", []):
            symbols_times = distribute_time_equally(word['start'], word['end'], word['text'])
            data_to_save["symbols"].extend(symbols_times)

    # Add consonant and vowel information
    data_to_save["symbols"] = add_consonant_vowel_info(data_to_save["symbols"], mapping_file)

    if save_to_file:
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)
        print(f"Results saved in: {json_output_path}")
    
    return data_to_save

# Example of use
audio_path = "test_audios/japanesef32.wav"
transcription_json = audio_query_json(audio_path, save_to_file=True)
