################################################### importing
from manim import *
from edge_tts import Communicate
import asyncio
from mutagen.mp3 import MP3
import icecream as debug
import re
from moviepy.editor import *
################################################### manim

class generator(Scene):

    def __init__(self, hook_code, title, body, main_code, run_times, **kwargs):
        
        super().__init__(**kwargs)

        self.hook_code = hook_code #string(location)
        self.title = title # string

        splitted_body = []
        index = 0
        last_space = 0
        for _ in range(len(body)):
            if body[_] == " ":
                last_space = _
            if (_ - index) >= 25:
                splitted_body.append(body[index:last_space])
                index = last_space + 1

        splitted_body.append(body[index:].strip())

        self.body = "\n".join(splitted_body) # string
        self.main_code = main_code # string(location)
        self.run_times = run_times # list of three runtimes (hook, title ,body)

    def construct(self):

        # defining mobjects

        #background
        _bg = Rectangle(width=9, height=16)
        _bg.set_fill("#252525", opacity=1)
        _bg.set_stroke(opacity=0)
        
        #hook code
        _hook_code = Code(
            f"{self.hook_code}",
            tab_width=7,
            language=str(((self.hook_code).split("."))[-1]),
            background="rectangle",
            background_config={"fill_color": "#141414", "stroke_opacity": 0},
            paragraph_config={"font": "monospace"},
            formatter_style="dracula"
        ).center().scale_to_fit_width(8)

        #title
        _title = Paragraph(
            f"{self.title}",
            font = "Comfortaa",
            alignment="center"
        ).scale_to_fit_width(7).center()

        #body
        _body = Text(
            self.body,
            font="Comfortaa",
            font_size=15
        ).scale_to_fit_width(8*0.9).to_edge(UP, buff=0.4)

        #body border
        _body_border = RoundedRectangle(
            width = 8, height = _body.height + 0.4,
            corner_radius=0.2,
            stroke_opacity = 0,
        ).to_edge(UP, buff=0.2).set_fill(color="#2e2e2e", opacity=1)

        #code
        _main_code = Code(
            f"{self.main_code}",
            tab_width=7,
            language=str(((self.main_code).split("."))[-1]),
            background="window",
            background_config={"fill_color": "#1A1A1A", "stroke_opacity": 0},
            paragraph_config={"font": "monospace"},
            formatter_style="dracula",
        ).center().scale_to_fit_width(8).next_to(_body_border, DOWN, buff=0.2)

        ####-----------------------------------------------
        self.next_section("hook")
        ##
        self.add(_bg, _hook_code)
        self.wait(self.run_times[0])
        self.remove(_hook_code)
        ##

        self.next_section("title")
        ##
        self.play(Write(_title), run_time = self.run_times[1])
        self.remove(_title)
        ##

        self.next_section("body")
        ##
        self.play(GrowFromEdge(_main_code, LEFT))
        self.add(_body_border)
        self.play(AddTextLetterByLetter(_body), run_time = self.run_times[2])
        self.wait(2)
        self.remove(_body, _body_border, _main_code)
        ##


################################################### generate audio and get duration

def generate_audios(texts): # texts is a list of texts, including hook, title, body

    names = ["hook", "title", "body"]
    run_times = []
    print("audio generation started")

    for name, text in zip(names, texts):
        
        mp3_path = f"./temp_files/{name}.mp3"
        text = " ".join(text.split("\n"))

        async def generate_audio(text = text, mp3_path = mp3_path):

            communicate = Communicate(text = text, voice = "en-IE-ConnorNeural")
            await communicate.save(mp3_path)

        asyncio.run(generate_audio())

        audio = MP3(mp3_path)
        run_times.append(audio.info.length)

    print('audio generation ended')
    return run_times

#################################################### merge audios with their respective clips

def merge_audios_videos(title):
    hook_audio = AudioFileClip("./temp_files/hook.mp3").volumex(5)
    hook_video = VideoFileClip("./media/videos/1920p60/sections/generator_0000_hook.mp4").set_audio(hook_audio)
    
    title_audio = AudioFileClip("./temp_files/title.mp3").volumex(5)
    title_video = VideoFileClip("./media/videos/1920p60/sections/generator_0001_title.mp4").set_audio(title_audio)

    body_audio = AudioFileClip("./temp_files/body.mp3").volumex(5)
    body_video = VideoFileClip("./media/videos/1920p60/sections/generator_0002_body.mp4").set_audio(body_audio)
 
    endvid = VideoFileClip("./media/videos/final_ending.mp4")

    final_video = concatenate_videoclips([hook_video, title_video, body_video, endvid])

    final_video.write_videofile(f"./final_videos/{"_".join(title.split())}.mp4", codec="libx264", audio_codec="aac")

    print(f"final video saved at: final_videos/{"_".join(title.split())}.mp4")

def main():

    # get video id
    with open("./temp_files/cwf.txt", "r", encoding="utf-8") as f:
        video_id = str(f.read())

    with open(f"./temp_files/{video_id}/title.txt", "r", encoding="utf-8") as f:
        title = f.read()
    with open(f"./temp_files/{video_id}/hook.txt", "r", encoding="utf-8") as f:
        hook = f.read()
    with open(f"./temp_files/{video_id}/body.txt", "r", encoding="utf-8") as f:
        body = f.read()
    with open(f"./temp_files/{video_id}/file_extension.txt", "r", encoding="utf-8") as f:
        file_ext = f.read()
    
    hook_code = f"./temp_files/{video_id}/hook_code.{file_ext}"
    main_code = f"./temp_files/{video_id}/main_code.{file_ext}"
    
    print("-------------------------------------------------")
    print(title)
    print(hook)
    print(body)
    print(file_ext)
    print(hook_code)
    print(main_code)
    print("-------------------------------------------------")

    from manim import tempconfig

    with tempconfig({
        "preview": False,
        "save_sections": True,
        "quality": "high_quality",
        "pixel_width": 1080,
        "pixel_height": 1920,
        "frame_width": 9,
        "frame_height": 16
    }):
        scene = generator(
            hook_code, 
            title, 
            body, 
            main_code, 
            generate_audios([hook, title, body])
            )
        scene.render()

    print("-------------------manim done!---------------------")

    merge_audios_videos(title)

if __name__ == "__main__":
    import shutil
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg is not installed. Manim will fail without it.")

    main()