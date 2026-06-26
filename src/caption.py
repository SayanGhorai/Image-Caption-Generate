import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import os
import gdown


MODEL_PATH = "models/final_model_epoch_3"
DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/12P6eYsHFP6UMdMjSkmT0TE9skC7xV0Re"


def download_model():
    """
    Download model folder from Google Drive if not already present.
    """
    if not os.path.exists(MODEL_PATH):
        os.makedirs("models", exist_ok=True)

        print("Downloading model from Google Drive...")
        gdown.download_folder(
            DRIVE_FOLDER_URL,
            output="models",
            quiet=False,
            use_cookies=False
        )
        print("Model downloaded successfully.")


class CaptionGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Download model if missing
        download_model()

        # Load processor
        self.processor = AutoProcessor.from_pretrained(
            MODEL_PATH,
            trust_remote_code=True
        )

        # Load merged fine-tuned model
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