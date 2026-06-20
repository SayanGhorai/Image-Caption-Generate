import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from peft import PeftModel
from PIL import Image


MODEL_NAME = "microsoft/Florence-2-large-ft"


class CaptionGenerator:
    def __init__(self, lora_path="models/florence_lora"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = AutoProcessor.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

        self.model = PeftModel.from_pretrained(
            base_model,
            lora_path
        )

        self.model.eval()

    def generate_caption(self, image_path):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            text="<CAPTION>",
            images=image,
            return_tensors="pt"
        ).to(
            self.device,
            torch.float16 if self.device == "cuda" else torch.float32
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=60,
            num_beams=4
        )

        caption = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]

        return caption