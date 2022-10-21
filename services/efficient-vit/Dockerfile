FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt update && apt install --no-install-recommends -y wget libgl1

# Install pip dependencies
RUN pip install torch==1.11.0+cpu torchvision==0.12.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install fastapi==0.78.0 opencv-python~=4.6.0.66 pyyaml==5.4.1 albumentations==0.5.2 efficientnet_pytorch==0.7.1 einops==0.3.0 uvicorn==0.18.2

# Clean cache
RUN pip cache purge
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Download pretrained models
RUN wget -O /app/efficient_vit.pth https://github.com/ControlNet/deepfake-demo/releases/download/efficientvit_model/efficient_vit.pth

# Copy files
COPY . .

# Download pretrained models
RUN python init.py

# RUN server
ENTRYPOINT python /app/main.py
