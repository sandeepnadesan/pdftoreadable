import streamlit as st
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
from PIL import Image
import fitz  # PyMuPDF for PDF handling
import os

# Create temp_files directory if it doesn't exist
if not os.path.exists("temp_files"):
    os.makedirs("temp_files")

# Function to extract text from image using OCR
def ocr_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to extract text from a PDF using OCR for non-machine-readable PDFs
def ocr_pdf(file_path):
    pages = convert_from_path(file_path)
    text = ""
    for page in pages:
        text += ocr_image(page)
    return text

# Function to extract text from a machine-readable PDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Streamlit interface
st.title("Non-Machine-Readable Document Conversion")

uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_type = uploaded_file.type
    file_path = os.path.join("temp_files", uploaded_file.name)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if "pdf" in file_type:
        # Check if the PDF is machine-readable
        text = extract_text_from_pdf(file_path)
        
        if len(text.strip()) == 0:
            st.write("This PDF is not machine-readable. Converting using OCR...")
            text = ocr_pdf(file_path)
        else:
            st.write("This PDF is already machine-readable.")
    else:
        # If an image file is uploaded
        image = Image.open(file_path)
        text = ocr_image(image)
    
    # Display the extracted text
    st.subheader("Extracted Text:")
    st.text_area("Text", text, height=300)

    # Option to download the extracted text
    if text:
        st.download_button(label="Download Extracted Text", data=text, file_name="extracted_text.txt", mime="text/plain")
    
    # Clean up temporary file
    os.remove(file_path)
