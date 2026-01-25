# Quick Start Guide - Unified Contract Analysis

## Overview

The system now has a unified endpoint `/api/analyze-contract` that:
1. Accepts PDF uploads
2. Extracts text and structured facts
3. Retrieves relevant knowledge base chunks (RAG)
4. Runs deterministic rule checks
5. Generates scholar-style ruling (with or without OpenAI)

## Running the Server

```bash
cd sharah-backend
source env/bin/activate
uvicorn main:app --reload
```

Server will start at: `http://localhost:8000`

## Testing the Endpoint

### With curl:

```bash
curl -X POST http://localhost:8000/api/analyze-contract \
  -F "file=@contract.pdf"
```

### Expected Response:

```json
{
  "success": true,
  "filename": "contract.pdf",
  "text_length": 5432,
  "verdict": "compliant" | "non-compliant" | "uncertain",
  "confidence": 85,
  "contract_type": "loan" | "murabaha" | "musharaka" | ...,
  "summary": "Brief summary...",
  "reasoning": "Detailed scholar-style reasoning...",
  "issues": [...],
  "missing_info_questions": [...],
  "evidence_used": [...],
  "extracted_facts": {...},
  "_metadata": {...}
}
```

## Running Tests

```bash
cd sharah-backend
source env/bin/activate
pytest tests/test_analyze_contract.py -v
```

Tests will pass even without OpenAI API key configured.

## Configuration

### With OpenAI (Recommended):

Create `.env` file:
```
OPENAI_API_KEY=your-key-here
```

### Without OpenAI:

System will still work but:
- Fact extraction uses heuristics (regex patterns)
- Scholar ruling is deterministic (no LLM)
- Verdict will be "uncertain" or "non-compliant" based on rule checks only

## API Documentation

Once server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Endpoints

- `POST /api/analyze-contract` - **NEW unified endpoint** (use this)
- `POST /api/shariah-check` - Structured input endpoint (still available)
- `POST /analyze` - **DEPRECATED** (old PDF endpoint, still works but use new one)
- `GET /health` - Health check

## Architecture

```
POST /api/analyze-contract
  ↓
routes/analyze_contract.py
  ↓
engine/orchestrator.py
  ├── PDF parsing (engine/pdf_parser.py)
  ├── Fact extraction (engine/facts_extractor.py)
  ├── KB loading (engine/kb_loader.py)
  ├── Chunk retrieval (engine/retrieval.py)
  ├── Rule checks (engine/rules.py)
  └── Scholar ruling (engine/scholar_llm.py)
  ↓
Response JSON
```

## Troubleshooting

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### PDF Parsing Errors
- Check PDF is not encrypted
- Ensure PDF contains extractable text (not just images)

### OpenAI Errors
- Check `.env` file exists and has valid API key
- System will fallback to heuristics if OpenAI fails

### Test Failures
- Tests use reportlab if available, otherwise minimal PDF bytes
- Install reportlab: `pip install reportlab` (optional, for better test PDFs)
