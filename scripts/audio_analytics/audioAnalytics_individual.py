import parselmouth
import matplotlib.pyplot as plt
import numpy as np

# Cargar un archivo de sonido
snd = parselmouth.Sound("/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/a_voice.wav")

# Análisis de formantes
formants = snd.to_formant_burg()

times = np.linspace(0, 3, 10000)
# Obtener los valores de F1 y F2 en un punto específico del tiempo
f1 = [formants.get_value_at_time(1, time) for time in times]  
f2 = [formants.get_value_at_time(2, time) for time in times]  

plt.plot(times, f1)
plt.plot(times, f2, label='f2')
plt.legend()
plt.show()