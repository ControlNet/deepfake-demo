import glob
import os
import pathlib
from urllib.request import urlopen

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response, JSONResponse
from starlette.staticfiles import StaticFiles

from inference import run_inference

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

checkpoint_path = "efficient_vit.pth"
config_file = "configs/architecture.yaml"


@app.get("/api/detect")
async def detect_deepfake(video) -> Response:
    video = video.replace("../wav2lip", os.environ["WAV2LIP_URL"] + "/static")
    if video.startswith("https://") or video.startswith("http://"):
        # download the video file from URL
        stream = urlopen(video).read()
        video = "temp.mp4"
        pathlib.Path(video).write_bytes(stream)

    try:
        confidence = str(float(run_inference(video, config_file, 0, checkpoint_path, 30, device)))
        return PlainTextResponse(confidence, 200)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return PlainTextResponse(None, 500)


@app.get("/api/real_samples")
async def get_real_samples() -> Response:
    face_list = glob.glob("samples/*.mp4")
    return JSONResponse({
        "samples": [f.replace("\\", "/") for f in face_list]
    }, 200)


if __name__ == '__main__':
    import uvicorn
    import argparse
    # add flag to run on cuda
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", action="store_true", help="run on cuda, default CPU")
    device = "cpu" if parser.parse_args().cuda is False else "cuda"

    uvicorn.run(app, port=7113, host="0.0.0.0")
