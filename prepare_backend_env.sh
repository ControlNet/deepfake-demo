#!/bin/bash

conda create --name deepfake_demo python=3.9 -y
conda activate deepfake_demo

conda install pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=11.3 ffmpeg -c pytorch -c conda-forge -y
conda install ffmpeg -c conda-forge -y
pip install fastapi==0.78.0 starlette==0.19.1 scipy==1.8.1 uvicorn==0.18.2 librosa==0.9.2 numpy~=1.22.0 opencv-python~=4.6.0.66 tqdm~=4.64.0 numba~=0.55.2 umap-learn visdom~=0.1.8.9 sounddevice~=0.4.3 SoundFile~=0.10.3.post1 Unidecode~=1.3.2 inflect~=5.3.0 PyQt5~=5.15.6 numba webrtcvad scikit-learn~=1.0.1 audioread~=2.1.9 pydantic~=1.9.1 matplotlib==3.3.0 albumentations==0.5.2 progress==1.5 pandas==1.2.4 pyyaml==5.4.1 einops==0.3.0 efficientnet_pytorch==0.7.1 python-multipart==0.0.5


# download pretrained models
wget -O services/rtvc/pretrained_models.zip https://github.com/ControlNet/deepfake-demo/releases/download/rtvc_model/pretrained.zip
unzip services/rtvc/pretrained_models.zip -d services/rtvc

wget -O services/wav2lip/wav2lip_gan.pth https://github.com/ControlNet/deepfake-demo/releases/download/wav2lip_model/wav2lip_gan.pth
wget -O services/efficient-vit/efficient_vit.pth https://github.com/ControlNet/deepfake-demo/releases/download/efficientvit_model/efficient_vit.pth
