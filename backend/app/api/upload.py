from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_validation import is_allowed_file
from app.services.upload_services import save_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV, XLSX, JSON allowed."
        )

    file_path = save_file(file)

    return {
        "filename": file.filename,
        "status": "uploaded",
        "path": file_path
    }
