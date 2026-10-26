import json
from fastapi import FastAPI, Depends, UploadFile, HTTPException, File
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db, engine, Base
from file_service import read_uploaded_file
from validation_service import validate_dataframe
from models import UploadedRecords


app = FastAPI(title="File Validation API")
Base.metadata.create_all(bind=engine)

@app.get('/api/health')
def health_check():
    return {
        "status": "success",
        "message": "File Validation API is Running"
    }

@app.get('/api/db-health')
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "success",
        "message": "PostgreSQL connection is working"
    }



@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    try:
        content = await file.read()
        df = read_uploaded_file(file.filename, content)
        records = validate_dataframe(df=df)
        db_records = [UploadedRecords(data=json.loads(json.dumps(record)), created_date=datetime.utcnow()) for record in records]
        db.add_all(db_records)
        db.commit()

        return {
            "status": "success",
            "message": "File validated and uploaded successfully",
            "records_inserted": len(db_records)
        }

    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Upload failed due to a server or database error"
        )

    finally:
        await file.close()


