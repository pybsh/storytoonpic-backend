import gc
import os

import PIL
import torch
from diffusers import AutoPipelineForImage2Image

import util


async def draw(file_dirs):
    device = "cuda" if torch.cuda.is_available() else "cup"
    if torch.backends.mps.is_available(): device = "mps"
    print(f"Using device: {device}")

    # pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    # pipeline = StableDiffusionXLPipeline.from_pretrained(
    #     "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    # )
    pipeline = AutoPipelineForImage2Image.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )

    pipeline = pipeline.to(device)
    pipeline.enable_attention_slicing()
    # pipeline.enable_model_cpu_offload()

    pipeline.load_lora_weights("ostris/crayon_style_lora_sdxl", weight_name="crayons_v1_sdxl.safetensors")
    # pipeline.load_lora_weights("ostris/super-cereal-sdxl-lora", weight_name="cereal_box_sdxl_v1.safetensors")

    for i, path in enumerate(file_dirs):
        prompt = f""
        negative_prompt = "NSFW"
        init_image = PIL.Image.open(path)
        init_image = PIL.ImageOps.exif_transpose(init_image)
        init_image = util.resize_image(init_image)

        # url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/img2img-sdxl-init.png"
        # init_image = load_image(url)
        image = pipeline(
            prompt,
            negative_prompt=negative_prompt,
            image=init_image,
            strength=0.4,
        ).images[0]
        if not os.path.isdir(f"{os.path.dirname(path)}/output/"):
            os.makedirs(f"{os.path.dirname(path)}/output/")
        image.save(f"{os.path.dirname(path)}/output/{i}.jpg")


if __name__ == "__main__":
    torch.cuda.empty_cache()
    gc.collect()
    draw(["./photo/test/1.jpg"])