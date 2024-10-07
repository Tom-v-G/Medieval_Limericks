import os
import moviepy.editor as mpy
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

if __name__ == "__main__":
    n = 4
    with open('temp/subjects.txt', 'w') as f:
        for i in range(n):
            f.write(input("Provide a limerick subject: ") + '\n')

    print('Generating Limericks')
    os.system("conda run -n CoCr python scripts/LLM.py")

    print('Generating Images')
    os.system(f"conda run -n Flux python scripts/FLUX.py -n {n}")

    print('Generating Sound')
    os.system(f"conda run -n TTS python scripts/AUDIO.py -n {n}")

    print('Creating Video')

    # Gather Limericks
    limericks = []
    for i in range(n):
        with open(f'temp/limerick_{i}.txt', 'r') as f:
            limericks.append("".join(f.readlines()))
    
    video_list = []
    
    FRONT_PADDING = 2 #seconds
    END_PADDING = 1 # seconds
    
    background_clip = mpy.ImageClip('data/background.png')
    background_clip.fps=24
    # bbackground_clip = background_clip.set_duration(8)

    for idx, limerick in enumerate(limericks):
        
        limerick = limerick.split("\n", maxsplit=1) #split on title
        
        # Video length depends on audio duration
        audio_clip = mpy.AudioFileClip(f"temp/audio_{idx}.wav")
        audio_duration = audio_clip.duration

        # Empty audio clips
        audio_front_pad = mpy.AudioClip(lambda x: 0, duration=FRONT_PADDING) #empty audio
        audio_end_pad = mpy.AudioClip(lambda x: 0, duration=END_PADDING) #empty audio

        full_audio = mpy.CompositeAudioClip([audio_front_pad, audio_clip, audio_end_pad])

        picture_clip = mpy.ImageClip(f'temp/image_{idx}.png')
        picture_clip.fps=24
        picture_clip = picture_clip.set_position((0.585, 'center'), relative=True).set_duration(audio_duration).set_start(0, True).crossfadein(FRONT_PADDING).crossfadeout(END_PADDING)
        picture_clip = picture_clip.resize(0.62)

        background_clip_2 =mpy.ImageClip('data/background2.png')
        background_clip.fps=24
        background_clip_2 = background_clip_2.set_duration(audio_duration).set_start(0, True).crossfadein(FRONT_PADDING).crossfadeout(END_PADDING)
        
        # Center the text on the left side of the screen 
        text_background = (mpy.ImageClip('data/background.png').crop(width = 960, height = 1080))

        title = limerick[0].replace("\"", '')
        title_clip = mpy.TextClip(f'{title}', fontsize=55)
        title_clip.fps=24
        title_clip = title_clip.set_duration(audio_duration).set_start(0, True).crossfadein(FRONT_PADDING).crossfadeout(END_PADDING)

        text_clip = mpy.TextClip(f'{limerick[1]}', fontsize=32)
        text_clip.fps=24
        text_clip = text_clip.set_duration(audio_duration).set_start(0, True).crossfadein(1).crossfadeout(1)
        
        text_video = mpy.CompositeVideoClip([
            text_background,
            title_clip.set_position(('center', 0.2), relative=True),
            text_clip.set_position(('center', 'center'), relative=True)
        ], size=(960, 1080))

        video = mpy.CompositeVideoClip([
            background_clip,
            background_clip_2,
            picture_clip,
            text_video
        ], size=(1920, 1080))

        
        video = video.set_duration(FRONT_PADDING + audio_duration + END_PADDING)
        video = video.set_audio(full_audio)
        video_list.append(video)

    if len(video_list) > 1: 
        final_video = mpy.concatenate_videoclips(video_list)
    else: final_video = video_list[0]

    background_audio = mpy.AudioFileClip(f'data/The-Medieval-Banquet.mp3')
    background_audio = (background_audio.set_end(final_video.end)
                        .volumex(0.15)
                        .audio_fadeout(1))

    final_audio = mpy.CompositeAudioClip([final_video.audio, background_audio])
    final_video = final_video.set_audio(final_audio)
    final_video.write_videofile("test3.mp4")