"""POST /api/analyze-contract endpoint."""

import logging

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from engine.orchestrator import analyze_contract_pdf

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["contract"])


@router.post("/analyze-contract")
async def analyze_contract(file: UploadFile = File(...)) -> JSONResponse:
    """
    Unified endpoint for contract analysis.
    
    Accepts PDF upload, extracts text, retrieves evidence, runs rule checks,
    and generates scholar ruling (with or without OpenAI).
    
    Returns consistent JSON schema with verdict, confidence, reasoning, issues, etc.
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF file."
        )
    
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded."
            )
        
        # Run analysis pipeline
        try:
            result = await analyze_contract_pdf(file_bytes, file.filename)
            return JSONResponse(status_code=200, content=result)
            
        except ValueError as e:
            # PDF parsing or validation errors
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            # Other analysis errors
            logger.exception(f"Analysis error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
