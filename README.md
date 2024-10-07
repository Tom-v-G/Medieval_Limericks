# Medieval Limerick Generator
By Emma Boom and Tom v. Gelooven 

[Example output](submission.mp4)

## Hardware requirements
This script has been tested on a laptop using an AMD Ryzen 7 6800H CPU and a NVIDIA GA104M GPU with 32GB of RAM.

## Setup
- Install the CoCr and Flux conda environments from the included yaml files
  Example: `conda install --file CoCr.yml` 
- download (ollama3.1)[https://github.com/ollama/ollama] and, from the shell, run the command `ollama run llama3` at least once. 
- download (Flux-schnell) [https://huggingface.co/black-forest-labs/FLUX.1-schnell]

## Running
Activate the `CoCr` conda environment and run `main.py` from the command line. You will be asked to provide four limerick subjects. Runtime can vary between 5 and 10 minutes
