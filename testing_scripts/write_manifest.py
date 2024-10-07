import os

with open(f'TTS_training_data/metadata.txt', 'w') as man:

    directory = 'TTS_training_data/wavs' # os.fsencode() 
    for file in [fi for fi in os.listdir(directory) if fi.endswith((".txt"))]:
        # print(file.strip('.txt'))
        # filename = os.fsdecode(file)
        
        with open(f'TTS_training_data/wavs/{file}', 'r') as f:
            text = f.readlines()
        man.write(f"{file.strip('.txt') + '.wav'} | {text}\n")    
        # print(text)



    
