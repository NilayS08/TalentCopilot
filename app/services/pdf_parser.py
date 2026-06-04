import fitz
import os

from fastapi import UploadFile

UPLOAD_DIR = "data/jds"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Save the uploaded file to the server
async def save_uploaded_file(file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)
    
    return file_path

# Extract text from the PDF file
def extract_text_from_pdf(pdf_path:str) -> str:
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()
    
    doc.close()
    return full_text