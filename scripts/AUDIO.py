import torch
import numpy
from TTS.api import TTS 
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num') 

    args = parser.parse_args()

    n = int(args.num)

    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Init TTS
    tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)

    # Gather Limericks
    limericks = []
    for i in range(n):
        with open(f'temp/limerick_{i}.txt', 'r') as f:
            limericks.append("".join(f.readlines()))

    # Run TTS
    for idx, limerick in enumerate(limericks): 
        tts.tts_to_file(text=limerick, file_path=f"temp/audio_{idx}.wav")
