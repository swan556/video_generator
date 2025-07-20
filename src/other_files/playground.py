from pydub import AudioSegment

# 1 second of silence
silence = AudioSegment.silent(duration=1000)  # duration in milliseconds

# Export as MP3
silence.export("silence.mp3", format="mp3")
