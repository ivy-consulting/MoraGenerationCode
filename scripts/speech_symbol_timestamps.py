# Standard library imports
import json

# Third-party library imports
import whisper_timestamped

# Local application imports
from auxiliar_functions_for_audio_query import distribute_time_equally, add_consonant_vowel_info, calculate_pitch

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
    print("Complete transcription:", result["text"])

    # Initialize the main dictionary to store the transcription and word details
    audio_query_data = {
        "transcription": result["text"],
        "words": []
    }

    # Process each word in the transcription
    for segment in result["segments"]:
        for word in segment.get("words", []):
            # Distribute time equally among the symbols of the word
            symbols_times = distribute_time_equally(word['start'], word['end'], word['text'])

            # Add consonant and vowel information to each symbol
            symbols_times = add_consonant_vowel_info(symbols_times, mapping_file)
            
            # Calculate and add pitch information to each symbol
            symbols_times = calculate_pitch(audio_path, symbols_times)

            # Create a dictionary for each word with its details
            word_detail = {
                "symbols": symbols_times,
                "is_interrogative": "か" in word['text'] or "?" in word['text'],  # Check if the word is interrogative
                "complete_word": word['text']
            }
            
            # Add the detailed word to the list
            audio_query_data["words"].append(word_detail)

    # Add additional metadata related to the audio processing
    metadata = {
        "speedScale": None,
        "pitchScale": None,
        "intonationScale": None,
        "volumeScale": None,
        "prePhonemeLength": None,
        "postPhonemeLength": None,
        "outputSamplingRate": 24000,  # Set the output sampling rate explicitly
        "outputStereo": None,
        "kana": result["text"]  # The transcribed text in Kana
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
    audio_path = "test_audios/japanesef32.wav"
    transcription_json = audio_query_json(audio_path, save_to_file=True)
