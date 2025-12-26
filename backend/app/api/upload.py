from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_validation import is_allowed_file
from app.services.upload_services import save_file
from app.services.parser import parse_file, FileParsingError

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV, XLSX, JSON allowed."
        )

    file_path = save_file(file)

    try:
        parsed = parse_file(file_path)
    except FileParsingError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "rows": parsed["rows"],
        "columns": parsed["columns"],
        "column_names": parsed["column_names"]
    }
