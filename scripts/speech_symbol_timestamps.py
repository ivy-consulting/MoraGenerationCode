import whisper_timestamped
import json
import os

def distribute_time_equally(start, end, text, decimals=4):
    """
    Distributes the time of a word among its symbols.
    """
    duration = end - start
    num_symbols = len(text)
    duration_per_symbol = duration / num_symbols
    symbols_times = []
    for i in range(num_symbols):
        symbol_start = start + i * duration_per_symbol
        symbol_end = start + (i + 1) * duration_per_symbol
        symbols_times.append({
            "symbol": text[i],
            "start": round(symbol_start, decimals),
            "end": round(symbol_end, decimals)
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
