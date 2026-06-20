import streamlit as st
import os
from src.pipeline import DrishtiPipeline


# Page config
st.set_page_config(
    page_title="Drishti - Multilingual Visual Assistant",
    page_icon="👁️",
    layout="wide"
)

st.title("👁️ Drishti")
st.subheader("Multilingual Visual Assistant for Bengali Accessibility")

st.write(
    "Upload an image to generate an English caption, "
    "translate it into Bengali, and listen to Bengali speech output."
)


# Load pipeline
@st.cache_resource
def load_pipeline():
    return DrishtiPipeline()


pipeline = load_pipeline()


# Upload image
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:
    temp_path = os.path.join("outputs/temp", uploaded_file.name)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(temp_path, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Generating..."):
        result = pipeline.run(temp_path)

    st.success("Done!")

    st.markdown("### English Caption")
    st.write(result["english_caption"])

    st.markdown("### বাংলা বিবরণ")
    st.write(result["bengali_caption"])

    st.markdown("### Bengali Audio")
    st.audio(result["audio_path"])