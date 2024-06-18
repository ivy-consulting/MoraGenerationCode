from fastapi import FastAPI
from scripts.speech_symbol_timestamps import audio_query_json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import soundfile as sf
import uvicorn


            

app = FastAPI()

def createBinary(audio_path):
  data, samplerate = sf.read(audio_path, dtype='int16')
  binary_data = data.tobytes()
  return binary_data, samplerate

@app.get("/mora")
def get_mora():
    
    audio_path = "./audio.wav"
    binary, samplerate = createBinary(audio_path)

    print("Binary data created", samplerate)

    data = audio_query_json(audio_path=audio_path, mapping_file="files/mapping.json")

    print("Data created")

    data_str = json.dumps(data)

    samplerate_str = str(samplerate)

    return  MultipartEncoder(
            fields={
                # JSONデータをテキストとして含める
                'data': ('data', data_str, 'application/json'),
                    
                'samplerate': ('samplerate', samplerate_str, 'text/plain')
            }
    )
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)