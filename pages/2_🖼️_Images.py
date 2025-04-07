import streamlit as st
from PIL import Image
import os
import base64
import io

st.set_page_config(page_title="Images", page_icon="🖼️")

# CSS with proper image containment
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .image-container {
        border: 2px solid #4a4a4a;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        transition: transform 0.2s;
        overflow: hidden;
    }

    .image-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .image-container img {
        width: 100% !important;
        height: auto !important;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

def img_to_bytes(img_path):
    img = Image.open(img_path)
    img = img.resize((800, 400))  # Optional: Set consistent dimensions
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return base64.b64encode(img_bytes.getvalue()).decode()

def image():
    st.title("Construction Progress Gallery")
    
    sheets = st.session_state.sheets
    df = sheets["images"]
    
    selected_station = st.session_state.get("selected_station", "Nadda")

    image_folder = "images"
    image_files = df["image"]

    # Full-width plan view
    with st.container():
        caption_html = f"""
        <p style="font-weight: bold; font-size: 24px; text-align: center; margin: 10px 0 20px 0;">
            {selected_station} Plan View
        </p>
        """
        st.image(os.path.join(image_folder, image_files[0]), use_container_width=True)
        st.markdown(caption_html, unsafe_allow_html=True)

    # Progress photos grid
    remaining_images = image_files[1:]
    
    for i in range(0, len(remaining_images), 2):
        cols = st.columns(2)
        row_images = remaining_images[i:i+2]
        
        for col_idx, img_file in enumerate(row_images):
            base_name = os.path.splitext(os.path.basename(img_file))[0]
            img_path = os.path.join(image_folder, img_file)
            with cols[col_idx]:
                try:
                    # Convert image to base64
                    b64_image = img_to_bytes(img_path)
                    
                    # Create HTML block with container and image
                    html = f"""
                    <div class="image-container">
                        <img src="data:image/png;base64,{b64_image}">
                        <p style="text-align: center; margin: 10px 0 0 0; font-weight: bold; font-size: 24px;">
                            Section: {base_name.upper()}
                        </p>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error loading {img_file}: {str(e)}")
    
if __name__ == "__main__":
    image()