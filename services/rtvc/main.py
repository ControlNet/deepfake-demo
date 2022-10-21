import glob
import os
import time
from asyncio import subprocess
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response, JSONResponse
from starlette.staticfiles import StaticFiles

from run_rtvc import load_models, run_voice_cloning

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="."), name="static")

enc_model_fpath = Path("encoder/saved_models/pretrained.pt")
syn_model_fpath = Path("synthesizer/saved_models/pretrained/pretrained.pt")
voc_model_fpath = Path("vocoder/saved_models/pretrained/pretrained.pt")
model_loaded = False


@app.get("/api/run_rtvc")
async def generate_audio(speaker_audio: str, text: str) -> Response:
    global model_loaded
    if not model_loaded:
        load_models(enc_model_fpath, voc_model_fpath, syn_model_fpath)
        model_loaded = True
    Path("out").mkdir(exist_ok=True)
    output_audio = f"out/{str(int(time.time()))[-10:]}.wav"
    try:
        run_voice_cloning(speaker_audio, text, output_audio)
        return PlainTextResponse(output_audio, 200)
    except Exception as e:
        print(e)
        return PlainTextResponse(None, 500)


@app.get("/api/aud_list")
async def get_audio_list() -> Response:
    aud_list = glob.glob("samples/*.wav")
    return JSONResponse({
        "audios": [f.replace("\\", "/") for f in aud_list]
    }, 200)


@app.post("/api/upload")
async def upload_audio_blob(file: UploadFile) -> Response:
    Path("recorded").mkdir(exist_ok=True)
    save_path = f"recorded/{str(int(time.time()))[-10:]}.webm"
    with open(save_path, "wb") as f:
        f.write(await file.read())
    wav_file = await convert_to_wav(save_path)
    os.remove(save_path)
    return JSONResponse({"file_name": wav_file}, 200)


async def convert_to_wav(webm_file: str):
    wav_file = webm_file.replace(".webm", ".wav")
    # convert webm to wav with 16000 sample rate
    ffmpeg_command = f"ffmpeg -i {webm_file} -ac 1 -ar 16000 {wav_file}"
    p = await subprocess.create_subprocess_shell(ffmpeg_command)
    await p.wait()
    return wav_file


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=7111, host="0.0.0.0")
