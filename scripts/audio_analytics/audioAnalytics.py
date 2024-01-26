import matplotlib
matplotlib.use('TkAgg')  # Usa el backend 'TkAgg' para interactividad
import matplotlib.pyplot as plt
import parselmouth
import numpy as np

# Rutas a los archivos de audio para cada vocal
vocales = ["a", "i", "u", "e", "o"]
archivos = [f"/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/{vocal}.wav" for vocal in vocales]

# Crear subplots para cada vocal
fig, axs = plt.subplots(5, 1, figsize=(10, 20))

for i, archivo in enumerate(archivos):
    # Cargar el archivo de audio
    snd = parselmouth.Sound(archivo)

    # Extraer la duración del audio
    duracion = snd.get_total_duration()

    # Definir los tiempos para el análisis desde el inicio hasta el final del audio
    times = np.linspace(0, duracion, int(duracion * 1000))  # 100 puntos por segundo

    # Obtener F1 y F2
    formants = snd.to_formant_burg()
    f1 = [formants.get_value_at_time(1, time) for time in times]
    f2 = [formants.get_value_at_time(2, time) for time in times]

    # Dibujar los formantes en el subplot correspondiente
    axs[i].plot(times, f1, label="F1")
    axs[i].plot(times, f2, label="F2")
    axs[i].set_title(f"Formantes para la vocal '{vocales[i]}'")
    axs[i].set_xlabel("Tiempo (s)")
    axs[i].set_ylabel("Frecuencia (Hz)")

    # Configurar los ticks del eje X para que estén cada 0.5 segundossudo apt-get install qt5-qmake qt5-default libqt5gui5 libqt5core5a libqt5widgets5 libqt5network5

    axs[i].set_xticks(np.arange(0, duracion + 0.1, 0.5))

    axs[i].legend()

# Ajustar el layout y mostrar la gráfica
plt.tight_layout()
plt.show()
