from gtts import gTTS
import os


class BengaliTTS:
    def __init__(self, output_dir="outputs/audio"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def text_to_speech(self, bengali_text, filename="output.mp3"):
        audio_path = os.path.join(self.output_dir, filename)

        tts = gTTS(
            text=bengali_text,
            lang="bn"
        )

        tts.save(audio_path)

        return audio_path