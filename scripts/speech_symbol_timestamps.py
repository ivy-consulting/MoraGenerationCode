import whisper_timestamped
import json
from auxiliar_functions_for_audio_query import distribute_time_equally, add_consonant_vowel_info, calculate_pitch

def audio_query_json(audio_path, save_to_file=False, json_output_path="speech_symbol_timestamps.json", mapping_file="files/mapping.json"):
    """
    Transcribes an audio file and adds consonant and vowel information to each symbol.
    """
    model = whisper_timestamped.load_model("base", device="cpu")
    result = whisper_timestamped.transcribe(model, audio_path, language="ja")
    print("Complete transcription:", result["text"])

    data_to_save = {
        "transcription": result["text"],
        "symbols": []
    }

    for segment in result["segments"]:
        for word in segment.get("words", []):
            print(word)
            symbols_times = distribute_time_equally(word['start'], word['end'], word['text'])
            data_to_save["symbols"].extend(symbols_times)

    # Add consonant and vowel information
    data_to_save["symbols"] = add_consonant_vowel_info(data_to_save["symbols"], mapping_file)

    # Calculate pitch for each symbol
    data_to_save["symbols"] = calculate_pitch(audio_path, data_to_save["symbols"])

    if save_to_file:
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)
        print(f"Results saved in: {json_output_path}")
    
    return data_to_save

# Example of use
audio_path = "test_audios/japanesef32.wav"
transcription_json = audio_query_json(audio_path, save_to_file=True)
