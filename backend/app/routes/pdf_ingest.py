from fastapi import APIRouter, UploadFile
from app.utils.file_utils import save_file
from app.services.pdf_ingest_service import process_pdf

router = APIRouter()

@router.post("/pdf")
async def upload_pdf(file: UploadFile):
    file_path = save_file(file)
    process_pdf(file_path)
    return {"status": "PDF processed", "filename": file.filename}
