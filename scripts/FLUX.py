import torch
from diffusers import FluxPipeline
from datetime import datetime as time
import argparse

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num') 

    args = parser.parse_args()

    n = int(args.num)

    # Gather limericks
    limericks = []
    for i in range(n):
        with open(f'temp/limerick_{i}.txt', 'r') as f:
            limericks.append("".join(f.readlines()))

    # Run local image generator
    model_id = "black-forest-labs/FLUX.1-schnell"

    pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    pipe.enable_sequential_cpu_offload()
    seed = 42

    for idx, prompt in enumerate(limericks):
        images = pipe(
                prompt,
                output_type="pil",
                num_inference_steps=4,
                generator=torch.Generator("cpu").manual_seed(seed)
                ).images
        images[0].save(f'temp/image_{idx}.png')

    
    