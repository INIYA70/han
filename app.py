import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image
from textblob import TextBlob

st.set_page_config(page_title="Handwriting to Typed Text", layout="centered")

st.title("📄 Handwriting to Typed Text")

uploaded_file = st.file_uploader("Upload a handwritten image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text... Please wait."):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(img_np, paragraph=True)

        corrected_paragraphs = []

        for (bbox, text, prob) in results:
            blob = TextBlob(text)
            corrected = str(blob.correct())
            corrected_paragraphs.append(corrected)

        final_output = "\n\n".join(corrected_paragraphs)

    st.subheader("📝 Final Output:")
    st.text_area("Formatted Corrected Text", final_output, height=400)

    st.download_button("📥 Download Typed Version", final_output, file_name="handwriting_output.txt")
