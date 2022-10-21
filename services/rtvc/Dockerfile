FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt update && apt install --no-install-recommends -y wget unzip libsndfile1

# Install pip dependencies
RUN pip install torch==1.11.0+cpu torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install fastapi==0.78.0 uvicorn==0.18.2 numpy==1.22.0 SoundFile~=0.10.3.post1 scipy==1.8.1 scikit-learn~=1.0.1 librosa==0.9.2 Unidecode~=1.3.2 inflect~=5.3.0 python-multipart==0.0.5 webrtcvad
RUN pip install -U matplotlib==3.6.1

# Clean cache
RUN pip cache purge
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Download pretrained models
RUN wget -O /app/pretrained_models.zip https://github.com/ControlNet/deepfake-demo/releases/download/rtvc_model/pretrained.zip
RUN unzip -o /app/pretrained_models.zip -d .

# Copy files
COPY . .

# RUN server
ENTRYPOINT python /app/main.py
