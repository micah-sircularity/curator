import os
from typing import Tuple
from io import BytesIO
from curatorai.utils.upload import upload_file_to_bucket
import fireworks.client
from fireworks.client.image import Answer, ImageInference


# Initialize the ImageInference client
fireworks.client.api_key = os.getenv("FIREWORKS_API_KEY")
inference_client = ImageInference(model="stable-diffusion-xl-1024-v1-0")

def generate_image(text: str, file_name: str) -> Tuple[Answer, str]:
    answer: Answer = inference_client.text_to_image(
        prompt=text,
        cfg_scale=7,
        height=1024,
        width=1024,
        sampler=None,
        steps=30,
        seed=0,
        safety_check=False,
        output_image_format="JPG",
    )

    if answer.image is None:
        raise RuntimeError(f"No return image, {answer.finish_reason}")
    
    answer.image.save("output.jpg")
    file_url = upload_file_to_bucket("output.jpg", "images", file_name)
        
    return answer, file_url

#generate_image(text="""A table of people enjoying a meal at a 
#waterfront restaurant, with the Ohio River in the background and the 
#city skyline in the distance""", file_name="pigbeach.jpg")


#answer, file_url
#= generate_image(text="""A table of people enjoying a meal at a 
#waterfront restaurant, with the Ohio River in the background and the 
#city skyline in the distance""", file_name="pigbeach.jpg")

#print(file_url)
