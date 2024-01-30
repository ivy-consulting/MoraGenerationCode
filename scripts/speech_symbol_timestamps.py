import whisper_timestamped
import json

# Carga el modelo de Whisper deseado
model = whisper_timestamped.load_model("base", device="cpu")

# Ruta al archivo de audio que deseas transcribir
audio_path = "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/japanes_1.mp3"

# Transcribe el archivo de audio
result = whisper_timestamped.transcribe(model, audio_path, language="ja")

# Imprime la transcripción completa
print("Transcripción completa:", result["text"])

# Función para dividir el tiempo de una palabra entre sus símbolos
def distribute_time_equally(start, end, text, decimals=4):
    duration = end - start
    num_symbols = len(text)
    duration_per_symbol = duration / num_symbols
    symbols_times = []
    for i in range(num_symbols):
        symbol_start = start + i * duration_per_symbol
        symbol_end = start + (i + 1) * duration_per_symbol
        symbols_times.append({
            "text": text[i],
            "start": round(symbol_start, decimals),
            "end": round(symbol_end, decimals)
        })
    return symbols_times


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
        "symbols": []
    }
    for word in segment.get("words", []):
        symbols_times = distribute_time_equally(word['start'], word['end'], word['text'])
        segment_info["symbols"].extend(symbols_times)
    data_to_save["segments"].append(segment_info)

# Define la ruta al archivo JSON donde se guardarán los resultados
json_output_path = "speech_symbol_timestamps.json"

# Guarda los datos en un archivo JSON
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

print(f"Resultados guardados en: {json_output_path}")
