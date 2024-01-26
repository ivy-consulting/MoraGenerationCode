import parselmouth
import numpy as np
import json

# Rutas a los archivos de audio y rangos de tiempo para cada vocal
vocales_info = {
    "a": {"archivo": "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/a.wav", "inicio": 1, "fin": 8.3},
    "e": {"archivo": "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/e.wav", "inicio": 1, "fin": 8.3},
    "i": {"archivo": "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/i.wav", "inicio": 1, "fin": 9},
    "o": {"archivo": "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/o.wav", "inicio": 1.3, "fin": 6},
    "u": {"archivo": "/home/andromeda/freelancer/AudioPhoneticsLab/test_audios/u.wav", "inicio": 1.5, "fin": 7.5}
}

# Diccionario para guardar los resultados
resultados = {}

for vocal, info in vocales_info.items():
    snd = parselmouth.Sound(info["archivo"])
    formants = snd.to_formant_burg()
    
    # Crear array de tiempos dentro del rango especificado
    times = np.linspace(info["inicio"], info["fin"], int((info["fin"] - info["inicio"]) * 1000))

    # Obtener los valores de F1 y F2
    f1_values = [formants.get_value_at_time(1, time) for time in times]
    f2_values = [formants.get_value_at_time(2, time) for time in times]

    # Filtrar y obtener los valores máximos y mínimos
    f1_max = np.nanmax(f1_values)
    f1_min = np.nanmin(f1_values)
    f2_max = np.nanmax(f2_values)
    f2_min = np.nanmin(f2_values)

    # Guardar los resultados
    resultados[vocal] = {
        "F1_max": f1_max,
        "F1_min": f1_min,
        "F2_max": f2_max,
        "F2_min": f2_min
    }

# Guardar los resultados en un archivo JSON
with open('/home/andromeda/freelancer/AudioPhoneticsLab/results/results_max_min_frecuency_per_vocal.json', 'w') as fp:
    json.dump(resultados, fp, indent=4)

print("Análisis completado y guardado en 'resultados_formantes.json'")
