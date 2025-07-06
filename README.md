# Video Generator
A simple manim based tool that I use to create educational Instagram reels. 

## features:
- Just Clone, download Manim, install dependencies, and run!
- A simple to use Window, where we can input parameters like:
  - title
  - hook of video
  - hook code
  - main body
  - main code
    and thats it, your video will be created in no time.
- You enter new data everytime, or load from already created data.
  Just click on the load button, and enter the id(its the title of video, all lowercase and where spaces are replaced by underscore)
  for example, if title was Custom Debug Function, then the video id is: custom_debug_function, which is also name of the final output video

## How to run?
- Install manim into your system: https://docs.manim.community/en/stable/installation.html
- Create a Virtual Env(if you want) and install all the dependencies using the following command: `pip install -r requirements.txt`
- head over to ./src/runner/code_runner.py
- run the code. That's it!

- Once you enter all the information, click on Submit button, and your video will be at location: ./final_videos

