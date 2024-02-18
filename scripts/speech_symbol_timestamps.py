# Standard library imports
import json

# Third-party library imports
import whisper_timestamped

# Local application imports
from auxiliar_functions_for_audio_query import (distribute_time_equally, add_consonant_vowel_info,
                                                 calculate_pitch, time_for_vowels_and_consonants, text_to_hiragana,
                                                 distribute_time_error_in_all_vowels_and_pauses, get_audio_duration)

def audio_query_json(audio_path, save_to_file=False, json_output_path="speech_symbol_timestamps.json", mapping_file="files/mapping.json"):
    """
    Transcribes an audio file to text, enriches each transcribed word with detailed phonetic information 
    (consonants and vowels), calculates the pitch for each symbol, and identifies interrogative sentences.
    
    Parameters:
    - audio_path (str): The path to the audio file for transcription.
    - save_to_file (bool): Whether to save the output to a JSON file. Defaults to False.
    - json_output_path (str): Path where the JSON output will be saved if save_to_file is True.
    - mapping_file (str): Path to the JSON file containing mappings for consonant and vowel information.
    
    Returns:
    - dict: A dictionary containing the complete transcription, word details including phonetic information, 
            pitch, and whether each word forms a question, along with some metadata about the audio processing.
    """
    # Load the model and transcribe the audio
    model = whisper_timestamped.load_model("base", device="cpu")
    result = whisper_timestamped.transcribe(model, audio_path, language="ja")
    print("Complete transcription:", text_to_hiragana(result["text"]))
    
    # Initialize the main dictionary to store the transcription and word details
    audio_query_data = {
        "transcription": text_to_hiragana(result["text"]),
        "accent_phrases": []
    }
    last_word_time = 0
    # Process each word in the transcription
    for segment in result["segments"]:
        for word in segment.get("words", []):
            # Convert the word to Kana
            word['text'] = text_to_hiragana(word['text'])
            # Verify the last word time
            if word['start'] == last_word_time:
                pause_mora = None
            else:
                pause_mora = word['start'] - last_word_time
            last_word_time = word['end']

            # Distribute time equally among the symbols of the word
            symbols_times = distribute_time_equally(word['start'], word['end'], word['text'])

            # Add consonant and vowel information to each symbol
            symbols_times = add_consonant_vowel_info(symbols_times, mapping_file)
            
            # Calculate and add pitch information to each symbol
            symbols_times = calculate_pitch(audio_path, symbols_times)

            # Calculate the vowels and consonants lenghts for each symbol
            symbols_times = time_for_vowels_and_consonants(symbols_times)
           
            # Create a dictionary for each word with its details
            word_detail = {
                "moras": symbols_times,
                "accent": 0,  # Default accent value
                "is_interrogative": "か" in word['text'] or "?" in word['text'],  # Check if the word is interrogative
                "complete_word": word['text'],
                "pause_mora": None if pause_mora is None else 
                {
                        "text": " ",
                        "consonant": None,
                        "consonant_length": None,
                        "vowel": "pau",
                        "vowel_length": pause_mora,
                        "pitch": 0.0
                    }
            }
            
            # Final pause of the word
            final_time = word['end']
            
            # Add the detailed word to the list
            audio_query_data["accent_phrases"].append(word_detail)
                     

    # Add additional metadata related to the audio processing
    metadata = {
        "final_pause": get_audio_duration(audio_path) - final_time if 
                        (get_audio_duration(audio_path) - final_time) > 0 else None,
        "speedScale": 1.0,
        "pitchScale": 0.0,
        "intonationScale": 1.0,
        "volumeScale": 1.0,
        "prePhonemeLength": 0.1,
        "postPhonemeLength": 0.1,
        "outputSamplingRate": 24000,  # Set the output sampling rate explicitly
        "outputStereo": False,
        "kana": text_to_hiragana(result["text"])  # The transcribed text in Kana
    }

    # Update the main dictionary with the metadata
    audio_query_data.update(metadata)

    # Save the results to a file if requested
    if save_to_file:
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(audio_query_data, json_file, ensure_ascii=False, indent=4)
        print(f"Results saved in: {json_output_path}")
    
    return audio_query_data

# Example usage
if __name__ == "__main__":
    audio_path = "test_audios/001-sibutomo (1).mp3"
    transcription_json = audio_query_json(audio_path, save_to_file=True)
