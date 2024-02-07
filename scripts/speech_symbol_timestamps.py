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

    audio_query_json = {
        "transcription": result["text"],
        "words": []
    }

    for segment in result["segments"]:
        for word in segment.get("words", []):
            
            # Distribute time equally per each  symbol
            symbols_times = distribute_time_equally(word['start'], word['end'], word['text'])

            # Add consonant and vowel information
            symbols_times = add_consonant_vowel_info(symbols_times, mapping_file)
            
            # Calculate pitch for each symbol
            symbols_times = calculate_pitch(audio_path, symbols_times)

            # Checking if the word is interrogative
            dic_per_word = {
                "symbols": symbols_times,
                "is_interrogative": "か" in word['text'] or "?" in word['text'],
                "complete_word": word['text']
                }
            
            # Add the word to the list of accent phrases
            audio_query_json["words"].append(dic_per_word)

    # Add metadata to json audio info
    metadata = {
        "speedScale": None,
        "pitchScale": None,
        "intonationScale": None,
        "volumeScale": None,
        "prePhonemeLength": None,
        "postPhonemeLength": None,
        "outputSamplingRate": 24000,
        "outputStereo": None,
        "kana": result["text"]
    }

    audio_query_json.update(metadata)

    if save_to_file:
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(audio_query_json, json_file, ensure_ascii=False, indent=4)
        print(f"Results saved in: {json_output_path}")
    
    return audio_query_json

# Example of use
audio_path = "test_audios/japanesef32.wav"
transcription_json = audio_query_json(audio_path, save_to_file=True)
