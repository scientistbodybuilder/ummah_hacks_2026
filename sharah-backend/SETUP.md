# SHARAH Backend Setup Guide

## Quick Start

### 1. Activate Virtual Environment

```bash
cd sharah-backend
source env/bin/activate
```

On Windows:
```bash
cd sharah-backend
env\Scripts\activate
```

### 2. Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

### 3. (Optional) Set OpenAI API Key

If you want to use the `/analyze` endpoint for PDF analysis, create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**Note:** The `/api/shariah-check` endpoint works without OpenAI API key. Only the `/analyze` PDF endpoint requires it.

### 4. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: `http://localhost:8000`

### 4. Test the API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Shariah Check:**
```bash
curl -X POST http://localhost:8000/api/shariah-check \
  -H "Content-Type: application/json" \
  -d '{
    "product_type": "revenue-based-advance",
    "interest_rate": 0,
    "profit_sharing_pct": 5,
    "terms_length_months": 12,
    "description": "VePay revenue-based advance: $50K advance against 5% of daily seller revenue, capped at $60K total repayment"
  }'
```

## Virtual Environment Details

- **Location:** `sharah-backend/env/`
- **Python Version:** 3.13.9
- **Activation:** `source env/bin/activate` (Unix/Mac) or `env\Scripts\activate` (Windows)

## Dependencies Installed

- fastapi>=0.104.0
- uvicorn[standard]>=0.24.0
- pydantic>=2.0.0
- python-dotenv>=1.0.0
- httpx>=0.25.0
- pytest>=7.4.0
- pytest-asyncio>=0.21.0
- openai>=1.0.0
- pymupdf>=1.24.0
- python-multipart>=0.0.6

## Running Tests

```bash
source env/bin/activate
pytest
```

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Troubleshooting

### Import Errors
- Make sure you're in the `sharah-backend/` directory
- Ensure virtual environment is activated
- Check that all dependencies are installed: `pip list`

### Port Already in Use
- Change the port: `uvicorn main:app --reload --port 8001`
- Or kill the process using port 8000: `lsof -ti:8000 | xargs kill`

### Knowledge Base Not Found
- Verify `data/shariah_kb/` directory exists
- Check that markdown files are present in the directory

### OpenAI API Key Warning
- If you see "Warning: OPENAI_API_KEY not set", this is normal
- The `/api/shariah-check` endpoint works without it
- Only the `/analyze` PDF endpoint requires OpenAI API key
- To use `/analyze`, create a `.env` file with your API key

### Virtual Environment Issues
- If `source env/bin/activate` doesn't work, try: `python3 -m venv env` to recreate it
- Then: `source env/bin/activate && pip install -r requirements.txt`
