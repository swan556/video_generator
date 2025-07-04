from manim import *

def main():
    class myclass(Scene):
        def construct(self):
            sq = Square(side_length=5)
            self.add(sq)

    with tempconfig({
        "preview": True,
        "save_sections": True,
        "quality": "high_quality",
        "pixel_width": 1080,
        "pixel_height": 1920,
        "frame_width": 9,
        "frame_height": 16
    }):
        scene = myclass()
        scene.render()

if __name__ == "__main__":
    main()