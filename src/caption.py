import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image


MODEL_PATH = "models/final_model_epoch_3"


class CaptionGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load local processor
        self.processor = AutoProcessor.from_pretrained(
            MODEL_PATH,
            trust_remote_code=True
        )

        # Load local merged fine-tuned model
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            trust_remote_code=True,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

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

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=60,
                num_beams=4,
                early_stopping=True
            )

        caption = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]

        return caption