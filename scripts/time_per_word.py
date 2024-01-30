import whisper_timestamped
import json

# Carga el modelo de Whisper deseado
model = whisper_timestamped.load_model("base", device="cpu")  # Usa "cpu" si no tienes GPU

# Ruta al archivo de audio que deseas transcribir
audio_path = "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/test_shikoku_thank_you_shikoku.wav"

# Transcribe el archivo de audio
result = whisper_timestamped.transcribe(model, audio_path, language="ja")

# Imprime la transcripción completa
print("Transcripción completa:", result["text"])

# Prepara los datos para guardarlos en JSON
data_to_save = {
    "transcription": result["text"],
    "segments": []
}

for segment in result["segments"]:
    segment_info = {
        "segment_id": segment['id'],
        "start": segment['start'],
        "end": segment['end'],
        "words": []
    }
    for word in segment.get("words", []):
        word_info = {
            "text": word['text'],
            "start": word['start'],
            "end": word['end'],
            "confidence": word['confidence']
        }
        segment_info["words"].append(word_info)
    data_to_save["segments"].append(segment_info)

# Define la ruta al archivo JSON donde se guardarán los resultados
json_output_path = "/home/andromeda/freelancer/AudioPhoneticsLab/vowel_detections.json"

# Guarda los datos en un archivo JSON
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

print(f"Resultados guardados en: {json_output_path}")
