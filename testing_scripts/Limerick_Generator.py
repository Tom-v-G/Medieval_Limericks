import torch
from diffusers import FluxPipeline
from datetime import datetime as time

import moviepy.editor as mpy
import gc

from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from TTS.api import TTS



class LLM:
    template_messages = [
        SystemMessage(content='''
                    You are an assistant that writes medieval limericks. Give the limerick a title. Only output the title and the limerick. Nothing else.
                    '''),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]

    model = Ollama(model="llama3:latest")
    prompt_template = ChatPromptTemplate.from_messages(template_messages)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    runnable = (
        {"text": RunnablePassthrough()} | prompt_template | model | StrOutputParser()
    )
 
def create_images(prompts):
    
    model_id = "black-forest-labs/FLUX.1-schnell"

    pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    pipe.enable_sequential_cpu_offload()
    seed = 42

    for idx, prompt in enumerate(prompts):
        images = pipe(
                prompt,
                output_type="pil",
                num_inference_steps=4,
                generator=torch.Generator("cpu").manual_seed(seed)
                ).images
        images[0].save(f'temp/{idx}.png')

def create_audio(limericks):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)
    for idx, limerick in enumerate(limericks):
        tts.tts_to_file(text=limerick, file_path=f"temp/{idx}.wav")

def generate_limerick(keywords):
    limericks = []
    for word in keywords:
        limericks.append(llm.runnable.invoke(word).split("\n", maxsplit=1))
    return limericks

if __name__ == '__main__':
    
    # Create Poems
    llm = LLM()
    limericks = generate_limerick(['spoon'])
    # llm.memory.clear()
    gc.collect()

    # Create images
    create_images(limericks)
    gc.collect()

    # Create audio
    create_audio(limericks)
    gc.collect()

    # Create Video
    video_list = []
    POEM_LENGTH = 8 #seconds 

    background_clip = mpy.ImageClip('background.png')
    background_clip.fps=24
    background_clip.set_duration(8)

    for idx, limerick in enumerate(limericks):

        picture_clip = mpy.ImageClip(f'{idx}.png')
        picture_clip.fps=24
        picture_clip = picture_clip.set_position((0.6, 'center'), relative=True).set_duration(5).set_start(2, True).crossfadein(1).crossfadeout(1)
        picture_clip = picture_clip.resize(0.7)
        
        title_clip = mpy.TextClip(f'{limerick[0]}', fontsize=55)
        title_clip.fps=24
        title_clip = title_clip.set_position((0.05, 0.2), relative=True).set_duration(5).set_start(2, True).crossfadein(1).crossfadeout(1)

        text_clip = mpy.TextClip(f'{limerick[1]}', fontsize=32)
        text_clip.fps=24
        text_clip = text_clip.set_position((0.05, 'center'), relative=True).set_duration(5).set_start(2, True).crossfadein(1).crossfadeout(1)


        video = mpy.CompositeVideoClip([
            background_clip,
            picture_clip,
            title_clip,
            text_clip
        ])

        video = video.set_duration(POEM_LENGTH)

        video_list.append(video)

    if len(video_list) > 1: final_video = mpy.concatenate_videoclips(video_list)
    else: final_video = video_list[0]

    final_video.write_videofile("test.mp4")
# final_clip = mpy.clips_array([clip, clip2])
# final_clip.resize(width=1920).write_videofile("poem.mp4")