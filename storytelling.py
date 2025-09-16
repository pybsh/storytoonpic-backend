import PIL
import torch
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration

import util


def storytelling(file_dirs):
    device = "cuda" if torch.cuda.is_available() else "cup"
    if torch.backends.mps.is_available(): device = "mps"
    print(f"Using device: {device}")

    model_id = "google/paligemma-3b-mix-224"
    dtype = torch.bfloat16

    images = []
    for path in file_dirs:
        image = PIL.Image.open(path)
        image = PIL.ImageOps.exif_transpose(image)
        image = util.resize_image(image,target_size=500)
        images.append(image)

    model = PaliGemmaForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=dtype,
        device_map=device,
        revision="bfloat16",
    ).eval()
    processor = AutoProcessor.from_pretrained(model_id)

    # Instruct the model to create a caption in Spanish
    prompt = "caption"
    model_inputs = processor(text=prompt, images=images, return_tensors="pt").to(model.device)
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        decoded = processor.decode(generation, skip_special_tokens=True)
        print(decoded)



if __name__ == '__main__':
    storytelling(["./photo/test/0.jpg","./photo/test/1.jpg","./photo/test/2.jpg","./photo/test/3.jpg"])
