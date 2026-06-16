from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.pdf_parser import save_uploaded_file
from app.services.pdf_parser import extract_text_from_pdf
from app.services.jd_extractor import extract_requirements

router = APIRouter(
    prefix="/jd",
    tags=["Job Description"],
)

@router.post("/upload")
async def upload_jd(
        file: UploadFile = File(...)
):
    file_path = await save_uploaded_file(file)
    extracted_text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "text": extracted_text
    }

# new endpoint to process the extracted JD text and return structured requirements
@router.post("/extract-requirements")
async def extract_jd_requirements(file: UploadFile = File(...)):
    file_path = await save_uploaded_file(file)
    jd_text = extract_text_from_pdf(file_path)

    requirements = extract_requirements(jd_text)

    return requirements