import whisper

# Carga el modelo de Whisper
model = whisper.load_model("base")  # Puedes elegir entre diferentes tamaños de modelo

# Transcribe un archivo de audio
result = model.transcribe("test_audios/japanes_1.mp3")

# Muestra la transcripción completa
print("Transcripción completa:")
print(result["text"])

# Muestra todas las propiedades disponibles en el resultado
print("\nTodas las propiedades disponibles del resultado de la transcripción:")
for key, value in result.items():
    print(f"{key}: {value}")
