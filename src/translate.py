# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch


# TRANSLATE_MODEL = "facebook/nllb-200-distilled-600M"


# class BengaliTranslator:
#     def __init__(self):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"

#         self.tokenizer = AutoTokenizer.from_pretrained(
#             TRANSLATE_MODEL
#         )

#         self.model = AutoModelForSeq2SeqLM.from_pretrained(
#             TRANSLATE_MODEL
#         ).to(self.device)

#         self.model.eval()

#     def translate_to_bengali(self, text):
#         inputs = self.tokenizer(
#             text,
#             return_tensors="pt"
#         ).to(self.device)

#         with torch.no_grad():
#             generated_tokens = self.model.generate(
#                 **inputs,
#                 forced_bos_token_id=self.tokenizer.convert_tokens_to_ids("ben_Beng"),
#                 max_length=100
#             )

#         bengali_text = self.tokenizer.batch_decode(
#             generated_tokens,
#             skip_special_tokens=True
#         )[0]

#         return bengali_text

from deep_translator import GoogleTranslator


class BengaliTranslator:
    def __init__(self):
        pass

    def translate_to_bengali(self, text):
        bengali_text = GoogleTranslator(
            source="en",
            target="bn"
        ).translate(text)

        return bengali_text