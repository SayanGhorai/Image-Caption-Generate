import streamlit as st
import os
from src.pipeline import DrishtiPipeline


# Page config
st.set_page_config(
    page_title="Drishti - Multilingual Visual Assistant",
    page_icon="👁️",
    layout="wide"
)


# Load pipeline
@st.cache_resource
def load_pipeline():
    return DrishtiPipeline()


pipeline = load_pipeline()


# Sidebar
with st.sidebar:
    st.title("👁️ About Drishti")

    st.markdown("""
    **Drishti** is an AI-powered multilingual visual assistant designed for Bengali accessibility.

    ### Features
    ✅ Image Caption Generation  
    ✅ English → Bengali Translation  
    ✅ Bengali Speech Output  
    ✅ Accessibility Support  

    ### Model Stack
    - Florence-2 Base (Fine-tuned with LoRA)
    - Helsinki-NLP (EN → BN)
    - gTTS (Bengali Voice)
    """)

    st.markdown("---")
    st.info("Built for visually impaired assistance.")


# Main Header
st.title("👁️ Drishti")
st.subheader("Multilingual Visual Assistant for Bengali Accessibility")

st.markdown("""
Upload an image and Drishti will:

1. Generate an English caption  
2. Translate it into Bengali  
3. Convert Bengali text into speech  
""")


# Upload section
uploaded_file = st.file_uploader(
    "📤 Upload an Image",
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

    with st.spinner("🔍 Processing image..."):
        result = pipeline.run(temp_path)

    with col2:
        st.success("✅ Processing Complete")

        st.markdown("### 📝 English Caption")
        st.write(result["english_caption"])

        st.markdown("### 🇧🇩 Bengali Caption")
        st.write(result["bengali_caption"])

        st.markdown("### 🔊 Bengali Audio")
        st.audio(result["audio_path"])


# Footer
st.markdown("---")
st.caption("Built with Florence-2, NLP Translation, and Text-to-Speech for Accessibility.")