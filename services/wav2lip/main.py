import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response, JSONResponse
import glob

from starlette.staticfiles import StaticFiles

from inference import run_wav2lip

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

checkpoint_path = "wav2lip_gan.pth"


@app.get("/api/run_wav2lip")
async def generate_video(face: str, audio: str) -> Response:
    Path("out").mkdir(exist_ok=True)
    output_video = f"out/{str(int(time.time()))[-10:]}.mp4"
    try:
        run_wav2lip(face, fps=30, resize_factor=1, rotate=False, crop=[0, -1, 0, -1], audio_file=audio,
            sample_rate=16000, checkpoint_path=checkpoint_path, outfile=output_video, box=[-1, -1, -1, -1],
            static=True, img_size=96, wav2lip_batch_size=128, face_det_batch_size=16, pads=[0, 10, 0, 0],
            nosmooth=False)
        return PlainTextResponse(output_video, 200)
    except Exception as e:
        print(e)
        return PlainTextResponse(None, 500)


@app.get("/api/face_list")
async def get_face_list() -> Response:
    face_list = glob.glob("samples/*.png")
    return JSONResponse({
        "faces": [f.replace("\\", "/") for f in face_list]
    }, 200)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=7112)
