from fastapi import FastAPI, File, UploadFile, HTTPException
from scripts.speech_symbol_timestamps import audio_query_json
import soundfile as sf
import uvicorn
import io

app = FastAPI()

def create_binary(file: UploadFile):
    data, samplerate = sf.read(io.BytesIO(file.file.read()), dtype='int16')
    binary_data = data.tobytes()
    return binary_data, samplerate

@app.post("/mora")
async def get_mora(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        binary, samplerate = create_binary(file)

        print("Binary data created", samplerate)

        # Save the uploaded file to a temporary path if needed
        # temp_audio_path = "./temp_audio.wav"
        # with open(temp_audio_path, "wb") as temp_file:
        #     temp_file.write(binary)

        # Get data using the audio_query_json function
        data = audio_query_json(audio_path=file.filename, mapping_file="files/mapping.json")

        print("Data created")

        response_data = {
            "data": data,
            "samplerate": samplerate
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500)
