from deep_translator import GoogleTranslator


class BengaliTranslator:
    def __init__(self):
        pass

    def translate_to_bengali(self, text):
        try:
            bengali_text = GoogleTranslator(
                source="en",
                target="bn"
            ).translate(text)

            return bengali_text

        except Exception as e:
            print("Translation Error:", e)
            return "বাংলা অনুবাদ পাওয়া যায়নি"