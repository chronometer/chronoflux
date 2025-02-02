import streamlit as st
import requests
from PIL import Image
import io
import time
import random

def call_flux_api(api_key, prompt, negative_prompt="", width=1024, height=1024, 
                 guidance_scale=3.0, seed=None, sampler="euler_a", steps=28):
    """Official Black Forest Labs Flux API integration with advanced parameters
    
    Args:
        api_key (str): Your Black Forest Labs API key
        prompt (str): Main prompt describing what you want to generate
        negative_prompt (str, optional): What to exclude from the image. Defaults to "".
        width (int, optional): Image width in pixels. Defaults to 1024.
        height (int, optional): Image height in pixels. Defaults to 1024.
        num_images (int, optional): Number of variations to generate. Defaults to 1.
        guidance_scale (float, optional): Creativity vs Precision. Lower=More Creative. Defaults to 3.0.
        seed (int, optional): Random seed for reproducibility. Defaults to None.
        sampler (str, optional): Sampling method to use. Defaults to "euler_a".
        steps (int, optional): Number of denoising steps. More=Higher quality but slower. Defaults to 28.
    
    Returns:
        tuple: (Image or list of Images, error message if any)
    """
    """Official Black Forest Labs Flux API integration"""
    base_url = "https://api.us1.bfl.ai/v1"
    headers = {
        "x-key": api_key,
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "guidance_scale": guidance_scale,
        "seed": seed,
        "sampler": sampler,
        "steps": steps
    }

    try:
        # Phase 1: Submit generation request
        st.write("Submitting image generation request...")
        response = requests.post(
            f"{base_url}/flux-pro-1.1",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        request_data = response.json()
        
        if "id" not in request_data:
            return None, "No request ID in response"
            
        request_id = request_data["id"]
        
        # Phase 2: Poll for result
        st.write("Waiting for image generation...")
        max_attempts = 60  # 30 seconds total (0.5s * 60)
        for _ in range(max_attempts):
            time.sleep(0.5)
            result = requests.get(
                f"{base_url}/get_result",
                headers=headers,
                params={"id": request_id}
            ).json()
            
            if result["status"] == "Ready":
                try:
                    # Get the image URL from the response
                    if "sample" in result["result"]:
                        img_url = result["result"]["sample"]
                    else:
                        img_url = result["result"]["samples"][0]
                        
                    # Download and return the image
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()
                    return Image.open(io.BytesIO(img_response.content)), None
                except Exception as e:
                    return None, f"Error processing API response: {str(e)}\nResponse: {result}"
            elif result["status"] == "Failed":
                return None, f"Generation failed: {result.get('error', 'Unknown error')}"
                
            st.write(f"Status: {result['status']}")
            
        return None, "Image generation timed out"

    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json()
            return None, f"API Error: {error_detail}"
        except:
            return None, f"API Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="ChronoFlux",
    page_icon="⌛",
    layout="centered"
)

st.title("⌛ ChronoFlux")
st.markdown("Create stunning AI-generated images with time-inspired prompts, powered by Black Forest Labs.")

api_key = st.text_input("API Key", value="7da1381b-6971-42be-9734-4ce2ff247f29", type="password")
prompt = st.text_area("Describe your image", height=100)

# Advanced Settings
with st.expander("🔧 Advanced Settings", expanded=False):
    # Image Quality Settings
    st.subheader("🎨 Image Quality")
    quality_col1, quality_col2 = st.columns(2)
    
    with quality_col1:
        steps = st.slider(
            "Quality Steps",
            min_value=20,
            max_value=50,
            value=28,
            step=1,
            help="More steps = higher quality but slower generation"
        )
        guidance_scale = st.slider(
            "Creativity vs Precision",
            0.0, 10.0, 3.0,
            step=0.1,
            help="Lower=More Creative, Higher=More Precise"
        )
    
    with quality_col2:
        sampler = st.selectbox(
            "Sampling Method",
            options=[
                "euler_a",  # Fast and good quality
                "euler",    # Similar to euler_a
                "heun",     # High quality but slower
                "dpm_2",    # Good for detailed images
                "dpm_2_a",  # Variant of dpm_2
                "lms"       # Linear multistep
            ],
            index=0,
            help="Different samplers affect image quality and generation style"
        )
        seed = st.number_input(
            "Random Seed",
            min_value=0,
            max_value=2**32-1,
            value=random.randint(0, 2**32-1),
            help="Set to same value for reproducible results"
        )
    
    # Image Content Settings
    st.subheader("🖼 Image Content")
    content_col1, content_col2 = st.columns(2)
    
    with content_col1:
        negative_prompt = st.text_area(
            "Negative Prompt",
            value="low quality, blurry, text, watermark",
            help="What you DON'T want in the image (comma separated)"
        )
    
    with content_col2:
        # Add aspect ratio presets
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            options=[
                "Square (1:1)",
                "Portrait (3:4)",
                "Landscape (4:3)",
                "Wide (16:9)",
                "Tall (9:16)"
            ],
            index=0,
            help="Choose image dimensions based on common aspect ratios"
        )
        
        # Set width and height based on aspect ratio
        if aspect_ratio == "Square (1:1)":
            width, height = 1024, 1024
        elif aspect_ratio == "Portrait (3:4)":
            width, height = 768, 1024
        elif aspect_ratio == "Landscape (4:3)":
            width, height = 1024, 768
        elif aspect_ratio == "Wide (16:9)":
            width, height = 1024, 576
        else:  # Tall (9:16)
            width, height = 576, 1024
            
        st.caption(f"Size: {width}x{height} pixels")

if st.button("Generate Image", type="primary"):
    if not prompt:
        st.error("Please enter a prompt first!")
    else:
        with st.spinner("🎨 Generating your masterpiece..."):
            image, error = call_flux_api(
                api_key=api_key,
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                guidance_scale=guidance_scale,
                seed=seed,
                sampler=sampler,
                steps=steps
            )
            
            if error:
                st.error(f"Error: {error}")
            elif image:
                st.success("✨ Generation Complete!")
                st.image(image, use_container_width=True)
