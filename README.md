# AudioPhoneticsLab

## Description

AudioPhoneticsLab is a project focused on generating audio queries using VOICEVOX Engine. It provides scripts to transcribe audio to text and then generate an audio query for text-to-speech synthesis, aiming to facilitate phonetic studies and applications.

## Installation

Before using the scripts in this repository, ensure you have Docker installed on your system as VOICEVOX Engine runs within a Docker container.

### Installing VOICEVOX Engine

To use VOICEVOX Engine, you need to pull its Docker image and run it on your machine. Follow these steps:

#### Pull VOICEVOX Engine Docker Image on Linux

Download the Docker image for VOICEVOX Engine:

```bash
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```
#### Run VOICEVOX Engine
Start the Docker container with VOICEVOX Engine:
```bash
docker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```

This command runs VOICEVOX Engine and maps port 50021 of the container to port 50021 of your local machine, allowing you to access the service from your browser or through HTTP requests.

#### Verify VOICEVOX Engine is Running
Once VOICEVOX Engine is running inside Docker, you can verify its operation by accessing the API documentation:

Open your browser and go to http://127.0.0.1:50021/docs. If you see the Swagger UI, VOICEVOX Engine is running correctly.

### Usage
To generate an audio query using the provided script, follow these steps:

Run the scripts.audio_query_with_voicevox.py script with the path to your audio file

### License
This project is licensed under the MIT License - see the LICENSE file for details.