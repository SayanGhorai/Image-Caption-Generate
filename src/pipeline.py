from src.caption import CaptionGenerator
from src.tts import BengaliTTS


class DrishtiPipeline:
    def __init__(self):
        self.caption_generator = CaptionGenerator()
        self.tts = BengaliTTS()

    def run(self, image_path):
        # Step 1: Generate English caption
        english_caption = self.caption_generator.generate_caption(image_path)

        # Temporary: Skip translation
        bengali_caption = english_caption

        # Step 2: Convert text to speech
        audio_path = self.tts.text_to_speech(bengali_caption)

        return {
            "english_caption": english_caption,
            "bengali_caption": bengali_caption,
            "audio_path": audio_path
        }