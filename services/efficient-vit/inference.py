import argparse
import glob
import os

import cv2
import numpy as np
import torch
import yaml
from albumentations import Compose, PadIfNeeded

from efficient_vit import EfficientViT
from transforms.albu import IsotropicResize


def create_base_transform(size):
    return Compose([
        IsotropicResize(max_side=size, interpolation_down=cv2.INTER_AREA, interpolation_up=cv2.INTER_CUBIC),
        PadIfNeeded(min_height=size, min_width=size, border_mode=cv2.BORDER_CONSTANT),
    ])


def read_video(video_path, frames_per_video, config):
    video_reader = cv2.VideoCapture(video_path)
    # read all frames
    frames = []
    while video_reader.isOpened():
        ret, frame = video_reader.read()
        if ret:
            transform = create_base_transform(config['model']['image-size'])
            frame = transform(image=frame)['image']
            if len(frame) > 0:
                frames.append(frame)
        else:
            break

    frames_number = len(frames)
    frames_interval = int(frames_number / frames_per_video)

    # Select only the frames at a certain interval
    if frames_interval > 0:
        frames = frames[::frames_interval]
    frames = frames[:frames_per_video]

    return np.array(frames)


_model = None


def get_or_load_model(model_path, config, efficient_net, device="cuda"):
    global _model
    if _model is None:
        if efficient_net == 0:
            channels = 1280
        else:
            channels = 2560

        if os.path.exists(model_path):
            _model = EfficientViT(config=config, channels=channels, selected_efficient_net=efficient_net)
            _model.load_state_dict(torch.load(model_path))
            _model.eval()
            _model.to(device)
        else:
            raise ValueError("No model found.")
    return _model


def run_inference(video_path, config_file, efficient_net, model_path, frames_per_video, device="cuda"):
    with open(config_file, 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)

    model = get_or_load_model(model_path, config, efficient_net, device)
    frames = read_video(video_path, frames_per_video, config)

    frames = np.transpose(frames, (0, 3, 1, 2))  # (B, C, H, W)

    x = torch.tensor(frames).float().to(device)
    with torch.no_grad():
        pred = model(x).sigmoid().mean().cpu().numpy()
    return pred


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--model_path', default='', type=str, metavar='PATH',
        help='Path to model checkpoint (default: none).')
    parser.add_argument('--max_videos', type=int, default=-1,
        help="Maximum number of videos to use for training (default: all).")
    parser.add_argument('--config', type=str,
        help="Which configuration to use. See into 'config' folder.")
    parser.add_argument('--efficient_net', type=int, default=0,
        help="Which EfficientNet version to use (0 or 7, default: 0)")
    parser.add_argument('--frames_per_video', type=int, default=30,
        help="How many equidistant frames for each video (default: 30)")

    opt = parser.parse_args()
    # label: original -> 0, fake -> 1

    for f in os.listdir("samples"):
        pred = run_inference(f"samples/{f}", opt.config, opt.efficient_net, opt.model_path,
            opt.frames_per_video)
        print(f, pred)

    for f in glob.glob("../wav2lip/out/*.mp4"):
        print(f, run_inference(f, opt.config, opt.efficient_net, opt.model_path,
            opt.frames_per_video))
