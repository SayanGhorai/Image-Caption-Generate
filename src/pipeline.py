from src.caption import CaptionGenerator
from src.translate import BengaliTranslator
from src.tts import BengaliTTS


class DrishtiPipeline:
    def __init__(self):
        self.caption_generator = CaptionGenerator()
        self.translator = BengaliTranslator()
        self.tts = BengaliTTS()

    def run(self, image_path):
        # Step 1: Generate English caption
        english_caption = self.caption_generator.generate_caption(image_path)

        # Step 2: Translate to Bengali
        bengali_caption = self.translator.translate_to_bengali(english_caption)

        # Step 3: Convert Bengali text to speech
        audio_path = self.tts.text_to_speech(bengali_caption)

        return {
            "english_caption": english_caption,
            "bengali_caption": bengali_caption,
            "audio_path": audio_path
        }