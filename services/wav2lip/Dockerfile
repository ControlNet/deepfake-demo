FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt update && apt install --no-install-recommends -y wget ffmpeg

# Install pip dependencies
RUN pip install torch==1.11.0+cpu torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install fastapi==0.78.0 uvicorn==0.18.2 python-multipart==0.0.5 opencv-python~=4.6.0.66 tqdm~=4.64.0 librosa==0.9.2

# Clean cache
RUN pip cache purge
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Download pretrained models
RUN wget -O /app/wav2lip_gan.pth https://github.com/ControlNet/deepfake-demo/releases/download/wav2lip_model/wav2lip_gan.pth

# Copy files
COPY . .

# Download pretrained models
RUN python init.py

# RUN server
ENTRYPOINT python /app/main.py
