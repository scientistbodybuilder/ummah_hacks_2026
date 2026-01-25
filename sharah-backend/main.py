"""FastAPI app entry point for SHARAH backend."""

import logging
import os
import fitz  # PyMuPDF
from io import BytesIO

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes import shariah_router
from engine.engine import analyze_shariah_compliance

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SHARAH API",
    description="Shariah compliance validation for Islamic financial products",
    version="1.0.0",
)

# CORS: allow frontend origins (local + production)
_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "https://sharah-frontend.vercel.app",
    "https://sharah.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(shariah_router)


def parse_pdf_text(file_bytes: bytes) -> str:
    """
    Parse text content from a PDF file.
    
    Args:
        file_bytes: Raw bytes of the PDF file
        
    Returns:
        Extracted text as a single string
    """
    text_parts = []
    
    # Open PDF from bytes
    pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        if text.strip():
            text_parts.append(text)
    
    pdf_document.close()
    
    return "\n\n".join(text_parts)


@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze a PDF document for Shariah compliance.
    
    Receives a PDF file, extracts text, and runs Shariah compliance analysis.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        JSON response with analysis results or error details
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF file."
        )
    
    try:
        # Read file contents
        logger.info(f"Processing file: {file.filename}")
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded."
            )
        
        # Parse PDF text
        logger.debug("Parsing PDF text...")
        try:
            extracted_text = parse_pdf_text(file_bytes)
            print("extracted text: ", extracted_text)
        except Exception as pdf_error:
            logger.error(f"PDF parsing error: {str(pdf_error)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse PDF: {str(pdf_error)}"
            )
        
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF. The file may be empty or contain only images."
            )
        
        logger.info(f"Extracted {len(extracted_text)} characters from PDF")
        logger.debug(f"First 500 chars: {extracted_text[:500]}")
        
        # Run Shariah compliance analysis
        logger.info("Running Shariah compliance analysis...")
        try:
            result = await analyze_shariah_compliance(extracted_text)
        except Exception as analysis_error:
            logger.error(f"Analysis error: {str(analysis_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(analysis_error)}"
            )
        
        # Check if result indicates an error from the engine
        if result.get("verdict") == "ERROR":
            logger.error(f"Engine returned error: {result.get('summary')}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": result.get("summary"),
                    "details": result
                }
            )
        
        logger.info(f"Analysis complete. Suggestion: {result.get('suggestion', 'N/A')}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "filename": file.filename,
                "text_length": len(extracted_text),
                "result": result
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.exception(f"Unexpected error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/health")
async def health() -> dict:
    """Health check for load balancers and monitoring."""
    return {"status": "ok", "service": "sharah-api"}
