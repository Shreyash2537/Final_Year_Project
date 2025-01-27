from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Load local model, processor, and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("models/vit-gpt2")
processor = ViTImageProcessor.from_pretrained("models/vit-gpt2")
tokenizer = AutoTokenizer.from_pretrained("models/vit-gpt2")

# Load an image
image = Image.open("example.jpg")

# Preprocess the image and generate captions
pixel_values = processor(images=image, return_tensors="pt").pixel_values
output_ids = model.generate(pixel_values, max_length=50, num_beams=4)
caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("Generated Caption:", caption)
