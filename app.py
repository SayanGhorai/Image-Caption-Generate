import streamlit as st
import os
from src.pipeline import DrishtiPipeline


# Page config
st.set_page_config(
    page_title="Multilingual Visual Assistant",
    page_icon="🖼️",
    layout="wide"
)


# Load pipeline
@st.cache_resource
def load_pipeline():
    return DrishtiPipeline()


pipeline = load_pipeline()


# Sidebar
with st.sidebar:
    st.title("About the Project")

    st.markdown("""
    This project is an AI-powered multilingual visual assistant designed to generate image captions, translate them into Bengali, and provide speech output for accessibility support.

    ### Dataset Used
    **COCO 2017 Dataset (Subset)**

    - Original Dataset: 118,287 images and 591,753 captions  
    - Validation Set: 5,000 images and 25,014 captions  
    - Fine-tuned on a subset of **50,000 training samples**  
    - Evaluated on **2,000 validation samples**  
    - Used for image caption generation with Florence-2 + LoRA  

    ### Features
    ✅ Image Caption Generation  
    ✅ English to Bengali Translation  
    ✅ Bengali Audio Output   
    """)

    st.markdown("---")
    st.info("Designed for assistive AI applications.")


# Main Header
st.title("Multilingual Visual Assistant")
st.subheader("Generate image descriptions with Bengali translation and speech output")

st.markdown("""
Upload an image and the system will:

1. Generate an English caption  
2. Translate it into Bengali  
3. Convert Bengali text into speech  
""")


# Upload section
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:
    os.makedirs("outputs/temp", exist_ok=True)

    temp_path = os.path.join("outputs/temp", uploaded_file.name)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            temp_path,
            caption="Uploaded Image",
            use_container_width=True
        )

    with st.spinner("Processing image..."):
        result = pipeline.run(temp_path)

    with col2:
        st.success("Processing Complete")

        st.markdown("### English Caption")
        st.write(result["english_caption"])

        st.markdown("### Bengali Caption")
        st.write(result["bengali_caption"])

        st.markdown("### Bengali Audio")
        st.audio(result["audio_path"])


# Footer
st.markdown("---")
st.caption("AI-Powered Multilingual Image Understanding System")