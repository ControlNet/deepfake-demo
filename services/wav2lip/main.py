import time
import os
from pathlib import Path

import cv2
from fastapi import FastAPI, UploadFile
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
    audio = f"{os.environ['RTVC_URL']}/static/{audio}"
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


@app.post("/api/upload")
async def upload_image_blob(file: UploadFile) -> Response:
    Path("recorded").mkdir(exist_ok=True)
    save_path = f"recorded/{str(int(time.time()))[-10:]}.png"
    with open(save_path, "wb") as f:
        f.write(await file.read())
    crop_face(save_path)
    return JSONResponse({"file_name": save_path}, 200)


face_cascade = None


def crop_face(save_path: str):
    global face_cascade
    if face_cascade is None:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(save_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    x, y, w, h = faces[0]
    center_x = x + w / 2
    center_y = y + h / 2
    side = max(w, h) * 1.5
    cropped = img[int(center_y - side / 2):int(center_y + side / 2), int(center_x - side / 2):int(center_x + side / 2)]
    resized = cv2.resize(cropped, (224, 224))
    cv2.imwrite(save_path, resized)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=7112, host="0.0.0.0")
