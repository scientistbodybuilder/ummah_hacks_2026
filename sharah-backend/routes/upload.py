"""PDF upload and application management endpoints."""

import logging
import io
import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])

# In-memory storage for applications (replace with database in production)
applications_db: List[dict] = []


class ApplicationResponse(BaseModel):
    id: str
    name: str
    date: str
    status: str


class ApplicationDetail(BaseModel):
    id: str
    name: str
    date: str
    status: str
    text_content: str


@router.post("/upload", response_model=ApplicationResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and extract its text content.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read the file content
        content = await file.read()
        
        # Parse PDF text
        pdf_reader = PdfReader(io.BytesIO(content))
        text_content = ""
        
        for page in pdf_reader.pages:
            text_content += page.extract_text() or ""
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Create application record
        application = {
            "id": str(uuid.uuid4())[:8].upper(),
            "name": file.filename.replace('.pdf', ''),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "text_content": text_content,
            "status": "pending"
        }
        
        # Store in memory
        applications_db.append(application)
        
        logger.info(f"Uploaded PDF: {application['name']} (ID: {application['id']})")
        
        return ApplicationResponse(
            id=application["id"],
            name=application["name"],
            date=application["date"],
            status=application["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error processing PDF: %s", e)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.get("/applications", response_model=List[ApplicationResponse])
async def get_applications():
    """
    Get all uploaded applications.
    """
    return [
        ApplicationResponse(
            id=app["id"],
            name=app["name"],
            date=app["date"],
            status=app["status"]
        )
        for app in applications_db
    ]


@router.get("/applications/{application_id}", response_model=ApplicationDetail)
async def get_application(application_id: str):
    """
    Get a specific application by ID with full text content.
    """
    for app in applications_db:
        if app["id"] == application_id:
            return ApplicationDetail(
                id=app["id"],
                name=app["name"],
                date=app["date"],
                status=app["status"],
                text_content=app["text_content"]
            )
    
    raise HTTPException(status_code=404, detail="Application not found")
