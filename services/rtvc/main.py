import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response, JSONResponse
import glob

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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=7111)
