import argparse
import os
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf
import torch

from encoder import inference as encoder
from synthesizer.inference import Synthesizer
from utils.argutils import print_args
from vocoder import inference as vocoder

synthesizer: Optional[Synthesizer] = None


def load_models(enc_model_fpath: Path, voc_model_fpath: Path, syn_model_fpath: Path):
    global synthesizer
    print("Preparing the encoder and the vocoder...")
    encoder.load_model(enc_model_fpath)
    vocoder.load_model(voc_model_fpath)
    # Load the models one by one.
    print("Preparing the encoder, the synthesizer and the vocoder...")
    synthesizer = Synthesizer(syn_model_fpath)


def run_voice_cloning(speaker_audio: str, text: str, output_audio: str, cpu=True):
    if cpu:
        # Hide GPUs from Pytorch to force CPU processing
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    print("Running a test of your configuration...\n")

    if torch.cuda.is_available():
        device_id = torch.cuda.current_device()
        gpu_properties = torch.cuda.get_device_properties(device_id)
        # Print some environment information (for debugging purposes)
        print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
              "%.1fGb total memory.\n" %
              (torch.cuda.device_count(),
              device_id,
              gpu_properties.name,
              gpu_properties.major,
              gpu_properties.minor,
              gpu_properties.total_memory / 1e9))
    else:
        print("Using CPU for inference.\n")

    print("Interactive generation loop")
    # Get the reference audio filepath
    in_fpath = speaker_audio

    # Computing the embedding
    # First, we load the wav using the function that the speaker encoder provides. This is
    # important: there is preprocessing that must be applied.

    # The following two methods are equivalent:
    # - Directly load from the filepath:
    preprocessed_wav = encoder.preprocess_wav(in_fpath)
    # - If the wav is already loaded:
    # original_wav, sampling_rate = librosa.load(str(in_fpath))
    # preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    print("Loaded file succesfully")

    # Then we derive the embedding. There are many functions and parameters that the
    # speaker encoder interfaces. These are mostly for in-depth research. You will typically
    # only use this function (with its default parameters):
    embed = encoder.embed_utterance(preprocessed_wav)
    print("Created the embedding")

    # Generating the spectrogram
    text = text

    # The synthesizer works in batch, so you need to put your data in a list or numpy array
    texts = [text]
    embeds = [embed]
    # If you know what the attention layer alignments are, you can retrieve them here by
    # passing return_alignments=True
    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]
    print("Created the mel spectrogram")

    # Generating the waveform
    print("Synthesizing the waveform:")

    # Synthesizing the waveform is fairly straightforward. Remember that the longer the
    # spectrogram, the more time-efficient the vocoder.
    generated_wav = vocoder.infer_waveform(spec, target=800, overlap=200)

    # Post-generation
    # There's a bug with sounddevice that makes the audio cut one second earlier, so we
    # pad it.
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

    # Trim excess silences to compensate for gaps in spectrograms (issue #53)
    generated_wav = encoder.preprocess_wav(generated_wav)

    # Save it on the disk
    filename = output_audio
    print(generated_wav.dtype)
    sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)

    print("\nSaved output as %s\n\n" % filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-s", "--speaker_audio", type=Path,
        help="Input speaker audio.")
    parser.add_argument("-t", "--text", type=str,
        help="Target text string.")
    parser.add_argument("-o", "--output_audio", type=Path,
        help="Output audio path.")
    args = parser.parse_args()
    args.enc_model_fpath = Path("encoder/saved_models/pretrained.pt")
    args.syn_model_fpath = Path("synthesizer/saved_models/pretrained/pretrained.pt")
    args.voc_model_fpath = Path("vocoder/saved_models/pretrained/pretrained.pt")
    args.cpu = True
    args.no_sound = True
    print_args(args, parser)
    load_models(args.enc_model_fpath, args.voc_model_fpath, args.syn_model_fpath)
    run_voice_cloning(args.speaker_audio, args.text, args.output_audio, args.cpu, args.no_sound)
