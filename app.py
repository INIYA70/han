import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2

st.title("📝 Handwritten Notes Reader (Image to Text)")

uploaded_file = st.file_uploader("Upload an image of handwritten notes", type=["png", "jpg", "jpeg"])

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['en'])  # Add other langs if needed

def preprocess_image(image: Image.Image):
    img = np.array(image.convert("L"))  # Convert to grayscale
    img = cv2.resize(img, (1024, 1024), interpolation=cv2.INTER_LINEAR)
    img = cv2.bilateralFilter(img, 11, 17, 17)
    return img

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    image = Image.open(uploaded_file)
    st.write("Processing...")

    processed_img = preprocess_image(image)
    reader = load_ocr_model()
    results = reader.readtext(processed_img)

    output_text = " ".join([res[1] for res in results])
    
    st.subheader("📄 Extracted Text:")
    st.text_area("Output", output_text, height=300)
