# SHARAH System Architecture Documentation

**Version:** 2.0  
**Last Updated:** January 2026  
**Purpose:** Complete system architecture for LLM understanding and development handoff

---

## 1. PROJECT OVERVIEW

### 1.1 What is SHARAH?

SHARAH is a **Shariah compliance validation API** for Islamic financial products. It analyzes product specifications (interest rates, profit-sharing terms, payment structures) against Islamic finance principles and returns compliance assessments with confidence scores, reasoning, and recommendations.

### 1.2 Core Value Proposition

- **Problem:** Islamic banks spend 3-5 weeks validating new products with Shariah scholars
- **Solution:** SHARAH validates products in <1 second using rule-based logic + RAG (Retrieval-Augmented Generation)
- **Impact:** Instant validation + scholar review optimization

### 1.3 Technology Stack

**Backend:**
- Python 3.13+
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- No database (stateless, file-based knowledge base)

**Frontend (separate repo):**
- Next.js 14
- React
- Tailwind CSS
- Vite

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Browser)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Frontend (Next.js - Separate Repo)           │   │
│  │  - Product Form                                       │   │
│  │  - Results Display                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬──────────────────────────────────────┘
                         │ HTTPS POST /api/shariah-check
                         │
┌────────────────────────▼──────────────────────────────────────┐
│              Backend (FastAPI - This Repo)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Layer (routes/)                                  │   │
│  │  - Request validation (Pydantic)                      │   │
│  │  - Error handling                                     │   │
│  │  - HTTP responses                                     │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼──────────────────────────────────┐   │
│  │  Service Layer (services/)                            │   │
│  │  - Interface to engine                                │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼──────────────────────────────────┐   │
│  │  Engine Layer (engine/)                                │   │
│  │  ┌────────────────────────────────────────────────┐   │   │
│  │  │  Shariah Engine (Rule-based logic)             │   │   │
│  │  │  - Feature extraction                           │   │   │
│  │  │  - Contract classification                      │   │   │
│  │  │  - Compliance checks                           │   │   │
│  │  │  - Confidence scoring                           │   │   │
│  │  └────────────────┬───────────────────────────────┘   │   │
│  │                   │                                    │   │
│  │  ┌────────────────▼───────────────────────────────┐   │   │
│  │  │  RAG System                                    │   │   │
│  │  │  - Knowledge base loader (rag_store.py)        │   │   │
│  │  │  - Retriever (retriever.py)                    │   │   │
│  │  │  - Reasoner (llm_reasoner.py)                  │   │   │
│  │  └────────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼──────────────────────────────────┐   │
│  │  Data Layer (data/)                                   │   │
│  │  - shariah_kb/ (Markdown files)                       │   │
│  │  - fatwas_database.json                               │   │
│  │  - product_examples.json                              │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow

```
1. Client → POST /api/shariah-check
   {
     "product_type": "revenue-based-advance",
     "interest_rate": 0.0,
     "profit_sharing_pct": 5.0,
     "terms_length_months": 12,
     "description": "VePay revenue-based advance..."
   }

2. routes/shariah_check.py
   - Validates request with Pydantic (ShariaCheckRequest)
   - Calls services/shariah_engine.check_shariah_compliance()

3. services/shariah_engine.py
   - Delegates to engine/shariah_engine.check_shariah_compliance()

4. engine/shariah_engine.py
   a) Feature Extraction
      - Extracts keywords from description
      - Identifies: interest words, profit-share words, asset words, etc.
   
   b) Contract Classification
      - Classifies as: loan_like, partnership_like, sale_like, or unclear
   
   c) Compliance Checks
      - Checks for Riba (interest) violations
      - Checks for Gharar (uncertainty)
      - Checks for late fees/penalties
      - Checks partnership guarantees
      - Checks asset backing for sales
   
   d) Confidence Scoring
      - Base: 65%
      - Adjusts based on classification clarity, issue severity, ambiguity
   
   e) RAG Integration
      - Loads knowledge base (rag_store.py)
      - Retrieves relevant chunks (retriever.py)
      - Adds evidence citations (llm_reasoner.py)
      - Generates follow-up questions
   
   f) Response Generation
      - Combines reasoning + evidence
      - Adds recommendations + questions
      - Returns ShariaCheckResponse

5. Response → Client
   {
     "is_shariah_compliant": true,
     "confidence": 80.0,
     "reasoning": "Classified structure as **partnership like**...",
     "flagged_issues": [],
     "applicable_fatwas": ["musharaka/mudaraba", "profit-sharing"],
     "recommendation": "Compliant based on provided information...",
     "evidence_used": ["gharar", "riba", "late_fees", "murabaha"]
   }
```

---

## 3. DIRECTORY STRUCTURE

```
ummah_hacks_2026/
├── sharah-backend/                    # Main backend application
│   ├── main.py                        # FastAPI app entry point
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile                     # Container configuration
│   ├── pytest.ini                     # Test configuration
│   │
│   ├── models/                        # Data models (Pydantic schemas)
│   │   ├── __init__.py
│   │   └── schemas.py                 # ShariaCheckRequest, ShariaCheckResponse
│   │
│   ├── routes/                        # API route handlers
│   │   ├── __init__.py                # Exports shariah_router
│   │   └── shariah_check.py           # POST /api/shariah-check endpoint
│   │
│   ├── services/                      # Service layer (interface to engine)
│   │   ├── __init__.py
│   │   └── shariah_engine.py          # Wrapper that calls engine
│   │
│   ├── engine/                        # Core compliance engine + RAG
│   │   ├── __init__.py                # Exports check_shariah_compliance
│   │   ├── shariah_engine.py          # Main compliance logic
│   │   ├── rag_store.py               # Knowledge base loader
│   │   ├── retriever.py               # Document retrieval (keyword-based)
│   │   └── llm_reasoner.py            # Evidence citation + question generation
│   │
│   ├── data/                          # Static data files
│   │   ├── fatwas_database.json       # Reference fatwas (future use)
│   │   ├── product_examples.json      # Example products
│   │   └── shariah_kb/                # Knowledge base (Markdown)
│   │       ├── riba.md                # Interest/riba rules
│   │       ├── murabaha.md            # Cost-plus sale rules
│   │       ├── musharaka.md           # Partnership rules
│   │       ├── gharar.md              # Uncertainty rules
│   │       └── late_fees.md           # Penalty rules
│   │
│   ├── tests/                         # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py                # Pytest fixtures
│   │   └── test_api.py                # API integration tests
│   │
│   └── docs/                          # Documentation
│       ├── API.md                     # API specification
│       ├── ARCHITECTURE.md            # Architecture notes
│       ├── SHARIAH_RULES.md           # Shariah rules reference
│       └── TESTING.md                 # Testing guide
│
├── client/                            # Frontend (separate repo, not detailed here)
│   └── ...
│
├── routes/                            # Legacy/other branch files (ignore)
│   └── shariahengine.py
│
├── README.md                          # Project README
└── TECHNICAL_DOCUMENTATION.md         # Original technical docs
```

---

## 4. COMPONENT DETAILS

### 4.1 API Layer (`routes/`)

**File:** `routes/shariah_check.py`

**Responsibilities:**
- HTTP request handling
- Request validation via Pydantic
- Error handling and HTTP status codes
- Response formatting

**Key Function:**
```python
@router.post("/api/shariah-check", response_model=ShariaCheckResponse)
async def shariah_check(request: ShariaCheckRequest) -> ShariaCheckResponse:
    """
    Validates Islamic financial product for Shariah compliance.
    Returns compliance assessment with confidence, reasoning, and recommendations.
    """
    result = await check_shariah_compliance(request)
    return result
```

**Error Handling:**
- `ValueError` → 400 Bad Request
- Other exceptions → 500 Internal Server Error (with logging)

### 4.2 Service Layer (`services/`)

**File:** `services/shariah_engine.py`

**Responsibilities:**
- Provides interface between API and engine
- Maintains separation of concerns
- Currently just delegates to engine

**Key Function:**
```python
async def check_shariah_compliance(request: ShariaCheckRequest) -> ShariaCheckResponse:
    """Delegates to engine.shariah_engine.check_shariah_compliance"""
    return await _check_shariah_compliance(request)
```

### 4.3 Engine Layer (`engine/`)

#### 4.3.1 Main Engine (`shariah_engine.py`)

**Core Logic Flow:**

1. **Feature Extraction** (`extract_features`)
   - Scans description for keywords
   - Returns `ExtractedFeatures` dataclass with boolean flags:
     - `has_interest_words`, `has_profit_share_words`, `has_asset_words`, etc.

2. **Contract Classification** (`classify_contract`)
   - Returns: `"loan_like"`, `"partnership_like"`, `"sale_like"`, or `"unclear"`
   - Logic:
     - `interest_rate > 0` → `loan_like`
     - `profit_sharing_pct > 0` → `partnership_like`
     - Asset/markup keywords → `sale_like`

3. **Compliance Checks** (`run_checks`)
   - Returns: `(is_compliant: bool, issues: List[str], fatwas: List[str])`
   - Checks:
     - **Riba:** Loan-like + interest → Non-compliant
     - **Late fees:** Flagged for review
     - **Gharar:** Uncertainty → Flagged
     - **Partnership guarantees:** Violates risk-sharing
     - **Sale asset clarity:** Needs asset details

4. **Confidence Scoring** (`score_confidence`)
   - Base: 65%
   - Adjustments:
     - Unclear contract: -20%
     - Clear classification: +5%
     - Riba detected: +15% (confident it's problematic)
     - Gharar: -15%
     - Late fees: -10%
     - Clean partnership: +10%

5. **Reasoning Generation** (`generate_reasoning`)
   - Combines classification, issues, fatwas, confidence
   - Human-readable explanation

6. **Recommendation Generation** (`generate_recommendation`)
   - Actionable next steps based on compliance status

7. **RAG Integration** (in `check_shariah_compliance`)
   - Loads knowledge base
   - Retrieves relevant evidence
   - Adds citations to reasoning
   - Generates follow-up questions

#### 4.3.2 RAG Store (`rag_store.py`)

**Responsibilities:**
- Loads markdown files from `data/shariah_kb/`
- Caches in memory (`_KB_CACHE`)
- Returns list of `DocChunk` objects

**Data Structure:**
```python
@dataclass(frozen=True)
class DocChunk:
    id: str          # File stem (e.g., "riba")
    source: str     # Relative path
    text: str       # Full markdown content
```

**Key Function:**
```python
def load_kb() -> List[DocChunk]:
    """Loads and caches knowledge base from data/shariah_kb/*.md"""
```

#### 4.3.3 Retriever (`retriever.py`)

**Responsibilities:**
- Keyword-based document retrieval (no embeddings)
- Simple tokenization and overlap scoring
- Returns top-k most relevant chunks

**Algorithm:**
1. Tokenize query and each chunk (lowercase, alphanumeric only)
2. Calculate intersection size (keyword overlap)
3. Sort by score (descending)
4. Return top-k chunks with score > 0

**Key Function:**
```python
def retrieve(query: str, chunks: List[DocChunk], k: int = 4) -> List[DocChunk]:
    """Returns top-k chunks by keyword overlap"""
```

#### 4.3.4 LLM Reasoner (`llm_reasoner.py`)

**Responsibilities:**
- Generates follow-up questions based on flagged issues
- Adds evidence citations to reasoning
- Enhances recommendations with questions

**Key Functions:**
```python
def build_missing_info_questions(flagged_issues: List[str], contract: str) -> List[str]:
    """Generates questions based on issues and contract type"""

def build_reasoning_with_evidence(base_reasoning: str, evidence: List[DocChunk]) -> str:
    """Appends evidence chunk IDs to reasoning"""

def build_recommendation_with_questions(base_recommendation: str, questions: List[str]) -> str:
    """Appends follow-up questions to recommendation"""
```

---

## 5. DATA MODELS

### 5.1 Request Schema (`models/schemas.py`)

```python
class ShariaCheckRequest(BaseModel):
    product_type: str              # "revenue-based-advance", "musharaka", etc.
    interest_rate: float           # 0-50 (annual %)
    profit_sharing_pct: float     # 0-50 (%)
    terms_length_months: int       # 1-120
    description: str               # 10-5000 chars
```

### 5.2 Response Schema

```python
class ShariaCheckResponse(BaseModel):
    is_shariah_compliant: bool     # True = Halal, False = Haram
    confidence: float               # 0-100%
    reasoning: str                 # Explanation
    flagged_issues: List[str]      # Specific issues found
    applicable_fatwas: List[str]  # Islamic principles (e.g., "riba", "musharaka")
    recommendation: str            # Next steps
    evidence_used: List[str]      # KB chunk IDs used
```

---

## 6. API ENDPOINTS

### 6.1 Health Check

```
GET /health
Response: {"status": "ok", "service": "sharah-api"}
```

### 6.2 Shariah Check

```
POST /api/shariah-check
Content-Type: application/json

Request Body:
{
  "product_type": "revenue-based-advance",
  "interest_rate": 0.0,
  "profit_sharing_pct": 5.0,
  "terms_length_months": 12,
  "description": "VePay revenue-based advance: $50K advance against 5% of daily seller revenue, capped at $60K total repayment"
}

Response:
{
  "is_shariah_compliant": true,
  "confidence": 80.0,
  "reasoning": "Classified structure as **partnership like**...",
  "flagged_issues": [],
  "applicable_fatwas": ["musharaka/mudaraba", "profit-sharing"],
  "recommendation": "Compliant based on provided information...",
  "evidence_used": ["gharar", "riba", "late_fees", "murabaha"]
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Validation error
- `500 Internal Server Error` - Server error

---

## 7. KEY ALGORITHMS

### 7.1 Contract Classification

```python
if interest_rate > 0:
    return "loan_like"
if interest_words AND fixed_repayment_words:
    return "loan_like"
if compounding_words:
    return "loan_like"
if profit_sharing_pct > 0 OR profit_share_words:
    return "partnership_like"
if asset_words OR markup_words OR product_type == "murabahah":
    return "sale_like"
return "unclear"
```

### 7.2 Compliance Decision

```python
is_compliant = True
if "Riba risk" in issues:
    is_compliant = False
```

### 7.3 Confidence Scoring

```python
base = 65.0
if contract == "unclear":
    base -= 20
else:
    base += 5
if "Riba risk" in issues:
    base += 15
if "Gharar risk" in issues:
    base -= 15
# ... more adjustments
return clamp(base, 0, 100)
```

### 7.4 Retrieval Algorithm

```python
query_tokens = tokenize(query.lower())
for chunk in chunks:
    chunk_tokens = tokenize(chunk.text.lower())
    score = len(query_tokens ∩ chunk_tokens)
    scored.append((score, chunk))
return top_k(scored, k=4)
```

---

## 8. KNOWLEDGE BASE

### 8.1 Structure

Markdown files in `data/shariah_kb/`:
- `riba.md` - Interest prohibition rules
- `murabaha.md` - Cost-plus sale rules
- `musharaka.md` - Partnership rules
- `gharar.md` - Uncertainty rules
- `late_fees.md` - Penalty rules

### 8.2 Format

Each file contains:
- Summary
- What to check
- Red flags (keywords)
- Missing info questions
- Notes

### 8.3 Loading

- Loaded once at first request
- Cached in memory (`_KB_CACHE`)
- No file I/O on subsequent requests

---

## 9. DEPENDENCIES

### 9.1 Core Dependencies

```
fastapi>=0.104.0          # Web framework
uvicorn[standard]>=0.24.0 # ASGI server
pydantic>=2.0.0           # Data validation
python-dotenv>=1.0.0     # Environment variables
httpx>=0.25.0             # HTTP client (for tests)
pytest>=7.4.0             # Testing framework
pytest-asyncio>=0.21.0    # Async test support
```

### 9.2 No External Services

- No database
- No external APIs
- No message queues
- Stateless design

---

## 10. CONFIGURATION

### 10.1 Environment Variables

- `DEBUG` - Set to "true" for debug logging (default: "false")

### 10.2 CORS Configuration

Allowed origins (in `main.py`):
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `https://sharah-frontend.vercel.app`
- `https://sharah.vercel.app`

---

## 11. ERROR HANDLING

### 11.1 Request Validation

- Pydantic automatically validates request body
- Returns 422 Unprocessable Entity for invalid data

### 11.2 Business Logic Errors

- `ValueError` → 400 Bad Request
- Other exceptions → 500 Internal Server Error
- All errors logged with full stack trace

### 11.3 File System Errors

- Missing knowledge base → `FileNotFoundError` (should not happen in production)
- Handled by engine, propagates as 500 error

---

## 12. TESTING

### 12.1 Test Structure

- `tests/test_api.py` - API integration tests
- `tests/conftest.py` - Pytest fixtures

### 12.2 Running Tests

```bash
cd sharah-backend
pytest
```

---

## 13. DEPLOYMENT

### 13.1 Docker

- `Dockerfile` included
- Build: `docker build -t sharah-backend .`
- Run: `docker run -p 8000:8000 sharah-backend`

### 13.2 Local Development

```bash
cd sharah-backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 13.3 Production

- Deploy to Railway, Render, or similar
- Set environment variables
- Ensure CORS origins match frontend

---

## 14. KEY DESIGN DECISIONS

### 14.1 Stateless Architecture

- No database
- No session storage
- Each request is independent
- Knowledge base cached in memory

### 14.2 Separation of Concerns

- **API Layer:** HTTP handling only
- **Service Layer:** Interface abstraction
- **Engine Layer:** Business logic
- **Data Layer:** Static files

### 14.3 RAG Implementation

- Simple keyword-based retrieval (no embeddings)
- Fast and deterministic
- Sufficient for MVP
- Can be upgraded to embeddings later

### 14.4 Rule-Based Engine

- Deterministic logic
- No ML models (yet)
- Transparent and explainable
- Fast execution

---

## 15. FUTURE ENHANCEMENTS

### 15.1 Potential Improvements

1. **Embeddings-based RAG**
   - Replace keyword matching with semantic search
   - Use sentence transformers or OpenAI embeddings

2. **ML Classification**
   - Train model on historical fatwas
   - Improve contract classification accuracy

3. **Database Integration**
   - Store request history
   - Track compliance trends
   - User accounts and saved products

4. **Enhanced Reasoning**
   - LLM integration for deeper analysis
   - Multi-step reasoning chains

5. **Real-time Updates**
   - WebSocket support for long-running analyses
   - Progress updates

---

## 16. IMPORT PATHS

### 16.1 Module Structure

```
sharah-backend/
├── main.py                    # FastAPI app
├── models/
│   └── schemas.py             # from models.schemas import ...
├── routes/
│   └── shariah_check.py       # from routes.shariah_check import ...
├── services/
│   └── shariah_engine.py      # from services.shariah_engine import ...
└── engine/
    ├── shariah_engine.py      # from engine.shariah_engine import ...
    ├── rag_store.py           # from engine.rag_store import ...
    ├── retriever.py           # from engine.retriever import ...
    └── llm_reasoner.py        # from engine.llm_reasoner import ...
```

### 16.2 Import Examples

```python
# In routes/shariah_check.py
from models.schemas import ShariaCheckRequest, ShariaCheckResponse
from services.shariah_engine import check_shariah_compliance

# In services/shariah_engine.py
from models.schemas import ShariaCheckRequest, ShariaCheckResponse
from engine.shariah_engine import check_shariah_compliance as _check_shariah_compliance

# In engine/shariah_engine.py
from models.schemas import ShariaCheckRequest, ShariaCheckResponse
from engine.rag_store import load_kb
from engine.retriever import retrieve
from engine.llm_reasoner import build_missing_info_questions, ...
```

---

## 17. CRITICAL FILES REFERENCE

### 17.1 Entry Point
- **`main.py`** - FastAPI app initialization, CORS, router mounting

### 17.2 API Layer
- **`routes/shariah_check.py`** - Single POST endpoint handler

### 17.3 Service Layer
- **`services/shariah_engine.py`** - Interface wrapper

### 17.4 Engine Core
- **`engine/shariah_engine.py`** - Main compliance logic (264 lines)
- **`engine/rag_store.py`** - Knowledge base loader
- **`engine/retriever.py`** - Document retrieval
- **`engine/llm_reasoner.py`** - Evidence and question generation

### 17.5 Data Models
- **`models/schemas.py`** - Request/response Pydantic models

### 17.6 Data Files
- **`data/shariah_kb/*.md`** - Knowledge base markdown files

---

## 18. UNDERSTANDING THE CODEBASE

### 18.1 Where to Start

1. **`main.py`** - Understand app setup
2. **`routes/shariah_check.py`** - See API endpoint
3. **`engine/shariah_engine.py`** - Core logic (start with `check_shariah_compliance`)
4. **`models/schemas.py`** - Understand data structures

### 18.2 Key Functions to Understand

1. **`check_shariah_compliance()`** - Main entry point (engine/shariah_engine.py:231)
2. **`extract_features()`** - Keyword detection (engine/shariah_engine.py:85)
3. **`classify_contract()`** - Contract type determination (engine/shariah_engine.py:100)
4. **`run_checks()`** - Compliance validation (engine/shariah_engine.py:128)
5. **`retrieve()`** - RAG retrieval (engine/retriever.py:14)

### 18.3 Data Flow Summary

```
Request → routes → services → engine → RAG → engine → services → routes → Response
```

---

## 19. COMMON TASKS

### 19.1 Adding a New Compliance Rule

1. Add keyword set in `engine/shariah_engine.py`
2. Update `extract_features()` to detect new keywords
3. Add check in `run_checks()`
4. Update confidence scoring if needed
5. Add knowledge base file in `data/shariah_kb/` if needed

### 19.2 Modifying Confidence Scoring

Edit `score_confidence()` in `engine/shariah_engine.py` (line 183)

### 19.3 Adding New Knowledge Base Files

1. Add `.md` file to `data/shariah_kb/`
2. File will be automatically loaded on next request
3. Clear cache by restarting server (or implement cache invalidation)

### 19.4 Changing API Response Format

1. Update `ShariaCheckResponse` in `models/schemas.py`
2. Update `check_shariah_compliance()` return statement
3. Update frontend if needed

---

## 20. TROUBLESHOOTING

### 20.1 Import Errors

- Ensure you're running from `sharah-backend/` directory
- Check Python path includes `sharah-backend/`
- Verify all `__init__.py` files exist

### 20.2 Knowledge Base Not Found

- Verify `data/shariah_kb/` exists relative to `engine/rag_store.py`
- Check file paths in `rag_store.py` (line 29-30)

### 20.3 CORS Errors

- Check allowed origins in `main.py` (line 23-28)
- Verify frontend URL matches

### 20.4 Low Confidence Scores

- Check contract classification logic
- Verify keyword detection is working
- Review confidence scoring adjustments

---

## END OF DOCUMENTATION

This document provides complete system architecture understanding. For specific implementation details, refer to the source code files listed in Section 17.

**Last Updated:** January 2026  
**Maintained By:** Development Team  
**Questions?** Refer to source code comments or technical documentation.
