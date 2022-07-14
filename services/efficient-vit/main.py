import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response, JSONResponse
import glob

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
    try:
        confidence = str(float(run_inference(video, config_file, 0, checkpoint_path, 30)))
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

    uvicorn.run(app, port=7113)
