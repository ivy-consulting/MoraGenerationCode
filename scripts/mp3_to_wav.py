from pydub import AudioSegment

# Cargar el archivo MP3
audio = AudioSegment.from_mp3("test_audios/230641vzpclfda (1).mp3")

# Convertir a WAV
audio.export("test_audios/file.wav", format="wav")
