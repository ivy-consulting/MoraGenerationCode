import whisper
import requests
import json

# Function to transcribe audio to text
def transcribe_audio_to_text(audio_path):
    """
    Transcribes audio to text using the Whisper model.

    Args:
    - audio_path (str): The file path to the audio file to be transcribed.

    Returns:
    - str: The transcribed text.
    """
    model = whisper.load_model("base")  # Load the base Whisper model
    result = model.transcribe(audio_path)
    print(result)
    return result["text"]

# Function to generate an audio query for VOICEVOX
def generate_voicevox_audio_query(text, speaker_id=1):
    """
    Generates an audio query for VOICEVOX.

    Args:
    - text (str): The text to synthesize.
    - speaker_id (int): The speaker ID for voice synthesis.

    Returns:
    - dict: The audio query response from VOICEVOX, or None if an error occurs.
    """
    voicevox_url = "http://127.0.0.1:50021/audio_query"
    params = {
        "text": text,
        "speaker": speaker_id
    }
    response = requests.post(voicevox_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main function
if __name__ == "__main__":
    audio_path = "test_audios/japanesef32.wav"  # Update this to the path of your .wav file
    speaker_id = 1  # Update this with the desired VOICEVOX speaker ID

    # Step 1: Transcribe the audio to text
    transcribed_text = transcribe_audio_to_text(audio_path)
    print("Transcribed Text:", transcribed_text)

    # Step 2: Generate the audio query with VOICEVOX
    audio_query = generate_voicevox_audio_query(transcribed_text, speaker_id)
    if audio_query:
        print("Audio Query Generated Successfully")
        # Save the query to a JSON file if necessary
        with open("audio_query.json", "w") as f:
            json.dump(audio_query, f, ensure_ascii=False, indent=4)
    else:
        print("Error generating the audio query")
