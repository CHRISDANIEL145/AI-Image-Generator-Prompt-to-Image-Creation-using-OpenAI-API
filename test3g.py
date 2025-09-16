import gradio as gr
import requests
from PIL import Image
from io import BytesIO

# OpenAI API key
API_KEY = "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"

# Function to generate image using OpenAI API
def generate_image(prompt, image_size, num_images):
    try:
        # Make a request to OpenAI's image generation API
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "n": int(num_images),
                "size": image_size
            }
        )
        
        # Handle response
        if response.status_code == 200:
            images = response.json().get("data", [])
            generated_images = []

            for img in images:
                img_url = img["url"]
                img_response = requests.get(img_url)
                image = Image.open(BytesIO(img_response.content))
                generated_images.append(image)
            
            return generated_images
        else:
            return f"Error: {response.json().get('error', {}).get('message', 'An error occurred.')}"
    except Exception as e:
        return f"An error occurred: {e}"

# Define the Gradio interface
description_input = gr.Textbox(label="Enter a Short Description", placeholder="E.g., A futuristic cityscape at sunset")
image_size_dropdown = gr.Dropdown(choices=["256x256", "512x512", "1024x1024"], value="512x512", label="Select Image Size")
num_images_slider = gr.Slider(minimum=1, maximum=5, value=1, step=1, label="Select Number of Images")

# Gradio Image Gallery Output
gallery = gr.Gallery(label="Generated Images")

# Build Gradio Interface
interface = gr.Interface(
    fn=generate_image,  # Function to call
    inputs=[description_input, image_size_dropdown, num_images_slider],
    outputs=gallery,
    title="AI Image Generator",
    description="Generate images based on your text descriptions using the OpenAI API.",
    theme="default"
)

# Run the Gradio Interface
if __name__ == "__main__":
    interface.launch()
