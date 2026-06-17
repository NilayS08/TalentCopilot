from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.pdf_parser import save_uploaded_file
from app.services.pdf_parser import extract_text_from_pdf
from app.services.resume_extractor import extract_candidate_profile

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):
    file_path = await save_uploaded_file(file)
    resume_text = extract_text_from_pdf(file_path)
    
    return {
        "filename":file.filename,
        "text":resume_text
    }

@router.post("/extract-profile")
async def extract_resume_profile(file: UploadFile = File(...)):
    file_path = await save_uploaded_file(file)
    resume_text = extract_text_from_pdf(file_path)

    profile = extract_candidate_profile(resume_text)

    return profile