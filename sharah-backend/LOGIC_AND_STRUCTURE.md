# SHARAH Backend - Complete Logic & Structure Documentation

**Purpose:** Complete technical documentation for LLM understanding of all components, engines, flows, and connections.

---

## 1. SYSTEM OVERVIEW

SHARAH has **TWO SEPARATE ENGINES** that serve different endpoints:

1. **Rule-Based Engine** (`engine/shariah_engine.py`) - Used by `/api/shariah-check`
   - Deterministic, keyword-based analysis
   - No OpenAI required
   - Structured input (product_type, interest_rate, etc.)

2. **OpenAI-Powered Engine** (`engine/engine.py`) - Used by `/analyze` (PDF upload)
   - Uses GPT-4o-mini for analysis
   - Requires OpenAI API key
   - Accepts free-form text (extracted from PDFs)

Both engines use **keyword-based RAG** to retrieve relevant knowledge base chunks, but they work differently.

---

## 2. COMPLETE REQUEST FLOWS

### 2.1 Flow 1: Structured API Endpoint (`/api/shariah-check`)

```
Client Request
    ↓
POST /api/shariah-check
{
  "product_type": "revenue-based-advance",
  "interest_rate": 0.0,
  "profit_sharing_pct": 5.0,
  "terms_length_months": 12,
  "description": "VePay revenue-based advance..."
}
    ↓
routes/shariah_check.py
  - Validates request with Pydantic (ShariaCheckRequest)
  - Calls services/shariah_engine.check_shariah_compliance()
    ↓
services/shariah_engine.py
  - Delegates to engine/shariah_engine.check_shariah_compliance()
    ↓
engine/shariah_engine.py (Rule-Based Engine)
  
  Step 1: Feature Extraction
    - extract_features(description)
    - Scans description for keywords
    - Returns ExtractedFeatures dataclass:
      * has_interest_words
      * has_profit_share_words
      * has_asset_words
      * has_late_fee_words
      * has_compounding_words
      * has_uncertainty_words
      * has_guarantee_words
      * etc.
  
  Step 2: Contract Classification
    - classify_contract(request, features)
    - Returns: "loan_like" | "partnership_like" | "sale_like" | "unclear"
    - Logic:
      * interest_rate > 0 → loan_like
      * profit_sharing_pct > 0 → partnership_like
      * asset/markup keywords → sale_like
  
  Step 3: Compliance Checks
    - run_checks(request, features, contract_type)
    - Checks for:
      * Riba (interest) violations
      * Gharar (uncertainty)
      * Late fees/penalties
      * Partnership guarantees
      * Asset backing for sales
    - Returns: (is_compliant: bool, issues: List[str], fatwas: List[str])
  
  Step 4: Confidence Scoring
    - score_confidence(request, contract_type, issues)
    - Base: 65%
    - Adjustments based on clarity, severity, ambiguity
  
  Step 5: Reasoning Generation
    - generate_reasoning(...)
    - Combines classification, issues, fatwas, confidence
  
  Step 6: RAG Integration
    - load_kb() → Loads all markdown files from data/shariah_kb/
    - retrieve(query, kb, k=4) → Keyword-based retrieval
      * Tokenizes query and chunks
      * Scores by keyword overlap
      * Returns top-4 matching chunks
    - build_reasoning_with_evidence(...) → Adds evidence citations
    - build_missing_info_questions(...) → Generates follow-up questions
    - build_recommendation_with_questions(...) → Adds questions to recommendation
  
  Step 7: Response Assembly
    - Returns ShariaCheckResponse:
      * is_shariah_compliant
      * confidence
      * reasoning (with evidence citations)
      * flagged_issues
      * applicable_fatwas
      * recommendation (with questions)
      * evidence_used (chunk IDs)
    ↓
Response to Client
{
  "is_shariah_compliant": true,
  "confidence": 80.0,
  "reasoning": "...",
  "flagged_issues": [],
  "applicable_fatwas": ["musharaka/mudaraba"],
  "recommendation": "...",
  "evidence_used": ["chunk_06_rbf_merchant_advance", ...]
}
```

### 2.2 Flow 2: PDF Upload Endpoint (`/analyze`)

```
Client Request
    ↓
POST /analyze
Content-Type: multipart/form-data
file: [PDF file bytes]
    ↓
main.py → analyze_document()
  
  Step 1: File Validation
    - Checks file extension is .pdf
    - Reads file bytes
    - Validates file is not empty
  
  Step 2: PDF Text Extraction
    - parse_pdf_text(file_bytes)
    - Uses PyMuPDF (fitz) library
    - Opens PDF from bytes stream
    - Extracts text from all pages
    - Returns concatenated text string
  
  Step 3: Text Validation
    - Checks extracted text is not empty
    - Logs text length and preview
  
  Step 4: OpenAI-Powered Analysis
    - Calls engine.engine.analyze_shariah_compliance(extracted_text)
      ↓
      engine/engine.py (OpenAI Engine)
      
      Sub-step 4a: Keyword-Based Chunk Retrieval
        - get_chunks(text)
        - Loops through all .md files in data/shariah_kb/
        - For each chunk:
          * extract_keywords_from_chunk(content)
            - Parses "Keywords: keyword1, keyword2, ..." from markdown
          * Checks if any keyword appears in text (word boundary matching)
          * If matches found, adds chunk to matching_chunks list
        - Returns list of matching chunks with metadata:
          {
            'filename': 'chunk_01_riba_core.md',
            'title': '# Riba (Interest) — Core Rule',
            'content': '...',
            'matched_keywords': ['interest', 'riba'],
            'all_keywords': ['interest', 'riba', 'apr', ...]
          }
      
      Sub-step 4b: Format Chunks for Context
        - format_chunks(chunks)
        - Formats matching chunks into structured context string
        - Each chunk gets header: "=== Relevant Shariah Source N: Title ==="
        - All chunks concatenated with separators
      
      Sub-step 4c: Construct OpenAI Prompt
        - System prompt: Defines SHARAH as expert analyzer
          * Lists core principles (Riba, Gharar, Maysir, Asset-backing)
          * Specifies JSON response format
        - User prompt: Contains:
          * Product/contract description (extracted PDF text)
          * Relevant Shariah knowledge base (formatted chunks)
        - Temperature: 0.2 (for consistency)
        - Response format: JSON object
      
      Sub-step 4d: Call OpenAI API
        - Checks if client is None (API key not set)
          * If None: Returns error response
        - Calls client.chat.completions.create()
          * Model: gpt-4o-mini (or provided model)
          * Messages: [system_prompt, user_prompt]
          * response_format: {"type": "json_object"}
        - Extracts response content
        - Parses JSON response
        - Adds metadata:
          * chunks_used: List of filenames
          * total_chunks_matched: Count
          * model_used: Model name
        - Returns analysis result
  
  Step 5: Error Handling
    - If OpenAI API fails: Returns error dict with verdict="ERROR"
    - If analysis returns error: Returns 500 status with error details
  
  Step 6: Success Response
    - Returns JSONResponse with:
      * success: true
      * filename: Original filename
      * text_length: Character count
      * result: Full analysis result from OpenAI
    ↓
Response to Client
{
  "success": true,
  "filename": "contract.pdf",
  "text_length": 5432,
  "result": {
    "suggestion": "compliant" | "non-compliant" | "uncertain",
    "confidence": 85,
    "summary": "...",
    "issues": [
      {
        "principle": "riba",
        "description": "...",
        "severity": "high"
      }
    ],
    "reasoning": "...",
    "_metadata": {
      "chunks_used": ["chunk_01_riba_core.md", ...],
      "total_chunks_matched": 3,
      "model_used": "gpt-4o-mini"
    }
  }
}
```

---

## 3. COMPONENT ARCHITECTURE

### 3.1 File Structure & Responsibilities

```
sharah-backend/
├── main.py                          # FastAPI app + PDF upload endpoint
├── openai_config.py                 # OpenAI client initialization (optional)
│
├── routes/
│   └── shariah_check.py            # POST /api/shariah-check handler
│
├── services/
│   └── shariah_engine.py           # Service layer (delegates to engine)
│
├── engine/                          # TWO ENGINES (different purposes)
│   ├── shariah_engine.py            # Rule-based engine (structured input)
│   ├── engine.py                   # OpenAI-powered engine (PDF/free-form)
│   ├── rag_store.py                # Knowledge base loader (used by rule-based)
│   ├── retriever.py                # Keyword-based retriever (used by rule-based)
│   └── llm_reasoner.py             # Evidence citation + questions (used by rule-based)
│
├── models/
│   └── schemas.py                  # Pydantic request/response models
│
└── data/
    └── shariah_kb/                  # Knowledge base (12 markdown chunks)
        ├── chunk_01_riba_core.md
        ├── chunk_02_gharar_uncertainty.md
        ├── chunk_03_riba_vs_murabaha.md
        ├── chunk_04_late_fees_ta_widh.md
        ├── chunk_05_profit_sharing_guarantee.md
        ├── chunk_06_rbf_merchant_advance.md
        ├── chunk_07_bnpl_late_fees_gharar.md
        ├── chunk_08_murabaha_asset_backing.md
        ├── chunk_09_guarantee_lou.md
        ├── chunk_10_gharar_vague_terms.md
        ├── chunk_11_musharaka_vs_mudaraba.md
        └── chunk_12_maysir_speculation.md
```

### 3.2 Component Dependencies

```
main.py
  ├── routes.shariah_router          → routes/shariah_check.py
  └── engine.engine                  → engine/engine.py (OpenAI engine)

routes/shariah_check.py
  ├── models.schemas                 → ShariaCheckRequest, ShariaCheckResponse
  └── services.shariah_engine        → services/shariah_engine.py

services/shariah_engine.py
  ├── models.schemas                 → ShariaCheckRequest, ShariaCheckResponse
  └── engine.shariah_engine          → engine/shariah_engine.py (Rule-based)

engine/shariah_engine.py (Rule-Based)
  ├── models.schemas                 → ShariaCheckRequest, ShariaCheckResponse
  ├── engine.rag_store              → load_kb()
  ├── engine.retriever              → retrieve()
  └── engine.llm_reasoner           → build_* functions

engine/engine.py (OpenAI-Powered)
  ├── openai_config                 → client, model
  └── (uses get_chunks, format_chunks internally)

engine/rag_store.py
  └── (reads from data/shariah_kb/*.md)

engine/retriever.py
  └── engine.rag_store              → DocChunk

engine/llm_reasoner.py
  └── engine.rag_store              → DocChunk
```

---

## 4. DETAILED ENGINE LOGIC

### 4.1 Rule-Based Engine (`engine/shariah_engine.py`)

**Purpose:** Deterministic compliance checking for structured product data

**Input:** `ShariaCheckRequest`
- product_type: str
- interest_rate: float
- profit_sharing_pct: float
- terms_length_months: int
- description: str

**Processing Pipeline:**

1. **Feature Extraction** (`extract_features`)
   ```python
   Keywords checked:
   - KW_INTEREST: {"interest", "apr", "rate", "percent interest", "coupon"}
   - KW_PROFIT_SHARE: {"profit share", "revenue share", "musharaka", ...}
   - KW_FIXED_REPAY: {"fixed repayment", "repay", "installment", ...}
   - KW_LATE_FEE: {"late fee", "penalty", "default fee", ...}
   - KW_COMPOUND: {"compound", "compounding"}
   - KW_ASSET: {"asset", "inventory", "equipment", "property", ...}
   - KW_UNCERTAIN: {"tbd", "may change", "variable at our discretion", ...}
   - KW_GUARANTEE: {"guarantee", "guaranteed return", "capital protected", ...}
   - KW_BUYBACK: {"buyback", "repurchase", "purchase option"}
   - KW_MARKUP: {"markup", "cost-plus", "murabaha"}
   ```

2. **Contract Classification** (`classify_contract`)
   ```python
   if interest_rate > 0:
       return "loan_like"
   if has_interest_words AND has_fixed_repayment_words:
       return "loan_like"
   if has_compounding_words:
       return "loan_like"
   if profit_sharing_pct > 0 OR has_profit_share_words:
       return "partnership_like"
   if has_asset_words OR mentions_markup_words OR product_type == "murabahah":
       return "sale_like"
   return "unclear"
   ```

3. **Compliance Checks** (`run_checks`)
   ```python
   Issues checked:
   - Loan-like + interest → Riba violation (non-compliant)
   - Late fee words → Flag for review
   - Uncertainty words → Gharar risk
   - Partnership + guarantee → Risk-sharing violation
   - Sale-like without asset words → Asset clarity issue
   - No structure info → Needs more info
   ```

4. **Confidence Scoring** (`score_confidence`)
   ```python
   base = 65.0
   if contract == "unclear": base -= 20
   else: base += 5
   if "Riba risk" in issues: base += 15
   if "Gharar risk" in issues: base -= 15
   if "Late fee" in issues: base -= 10
   if clean partnership: base += 10
   return clamp(base, 0, 100)
   ```

5. **RAG Integration**
   - Uses `rag_store.load_kb()` to load all chunks
   - Uses `retriever.retrieve()` for keyword-based search
   - Uses `llm_reasoner` functions to enhance output

**Output:** `ShariaCheckResponse`

### 4.2 OpenAI-Powered Engine (`engine/engine.py`)

**Purpose:** LLM-powered analysis for free-form text (PDFs)

**Input:** `text: str` (extracted from PDF)

**Processing Pipeline:**

1. **Chunk Retrieval** (`get_chunks`)
   ```python
   For each .md file in data/shariah_kb/:
     - Read file content
     - Extract keywords (parse "Keywords: ..." line)
     - Check if any keyword matches text (word boundary regex)
     - If matches: Add to matching_chunks with metadata
   Return: List of matching chunk dicts
   ```

2. **Chunk Formatting** (`format_chunks`)
   ```python
   For each matching chunk:
     - Create header: "=== Relevant Shariah Source N: Title ==="
     - Append full chunk content
   Return: Formatted string with all chunks
   ```

3. **Prompt Construction**
   ```python
   system_prompt = """
   You are SHARAH, expert Islamic finance analyzer.
   Principles: Riba, Gharar, Maysir, Asset-backing
   Respond in JSON format:
   {
     "suggestion": "compliant" | "non-compliant" | "uncertain",
     "confidence": 0-100,
     "summary": "...",
     "issues": [{"principle": "...", "description": "...", "severity": "..."}],
     "reasoning": "..."
   }
   """
   
   user_prompt = f"""
   Analyze this product/contract:
   {text}
   
   Relevant Shariah knowledge:
   {formatted_chunks}
   """
   ```

4. **OpenAI API Call**
   ```python
   response = await client.chat.completions.create(
       model="gpt-4o-mini",
       messages=[system_prompt, user_prompt],
       response_format={"type": "json_object"},
       temperature=0.2
   )
   ```

5. **Response Processing**
   - Parse JSON from response
   - Add metadata (chunks_used, model_used)
   - Return analysis dict

**Output:** `dict` with analysis results

---

## 5. RAG SYSTEMS

### 5.1 Rule-Based Engine RAG (`rag_store.py` + `retriever.py`)

**Knowledge Base Loading:**
- `rag_store.load_kb()`: Loads all `.md` files from `data/shariah_kb/`
- Caches in memory (`_KB_CACHE`)
- Returns `List[DocChunk]` where each chunk has:
  - `id`: Filename stem (e.g., "chunk_01_riba_core")
  - `source`: Relative path
  - `text`: Full markdown content

**Retrieval Algorithm:**
- `retriever.retrieve(query, chunks, k=4)`
- Tokenizes query and each chunk (lowercase, alphanumeric only)
- Scores by keyword overlap: `len(query_tokens ∩ chunk_tokens)`
- Sorts by score (descending)
- Returns top-k chunks with score > 0

**Usage:**
- Query: `f"{product_type}\n{description}"`
- Returns top 4 most relevant chunks
- Evidence IDs added to reasoning

### 5.2 OpenAI Engine RAG (`engine.py` internal)

**Knowledge Base Access:**
- Direct file reading (no caching)
- `get_chunks(text)`: Scans all `.md` files
- Extracts keywords from each chunk
- Matches keywords against input text

**Keyword Extraction:**
- Parses "Keywords: keyword1, keyword2, ..." from markdown
- Uses regex word boundary matching
- Returns chunks with any matching keywords

**Usage:**
- All matching chunks formatted into context
- Passed to OpenAI as part of prompt
- Chunk filenames included in metadata

---

## 6. KNOWLEDGE BASE STRUCTURE

### 6.1 File Format

Each markdown file in `data/shariah_kb/` follows this structure:

```markdown
# Title

Keywords: keyword1, keyword2, keyword3, ...

## Section 1
Content...

## Section 2
Content...
```

**Example:** `chunk_01_riba_core.md`
```markdown
# Riba (Interest) — Core Rule

Keywords: interest, riba, apr, rate, compounding, fixed repayment, coupon

## Summary
A loan that requires repayment with any guaranteed excess (interest/APR/coupon) is prohibited.

## What to check
- Is this money-for-money with extra repayment?
...
```

### 6.2 Available Chunks

1. `chunk_01_riba_core.md` - Core interest prohibition rules
2. `chunk_02_gharar_uncertainty.md` - Uncertainty rules
3. `chunk_03_riba_vs_murabaha.md` - Interest vs cost-plus distinction
4. `chunk_04_late_fees_ta_widh.md` - Penalty handling
5. `chunk_05_profit_sharing_guarantee.md` - Partnership guarantees
6. `chunk_06_rbf_merchant_advance.md` - Revenue-based financing
7. `chunk_07_bnpl_late_fees_gharar.md` - BNPL specific issues
8. `chunk_08_murabaha_asset_backing.md` - Asset backing requirements
9. `chunk_09_guarantee_lou.md` - Guarantee rules
10. `chunk_10_gharar_vague_terms.md` - Vague terms
11. `chunk_11_musharaka_vs_mudaraba.md` - Partnership types
12. `chunk_12_maysir_speculation.md` - Speculation prohibition

---

## 7. API ENDPOINTS

### 7.1 Health Check

```
GET /health
Response: {"status": "ok", "service": "sharah-api"}
```

### 7.2 Structured Shariah Check

```
POST /api/shariah-check
Content-Type: application/json

Request:
{
  "product_type": "revenue-based-advance",
  "interest_rate": 0.0,
  "profit_sharing_pct": 5.0,
  "terms_length_months": 12,
  "description": "..."
}

Response:
{
  "is_shariah_compliant": true,
  "confidence": 80.0,
  "reasoning": "...",
  "flagged_issues": [],
  "applicable_fatwas": ["musharaka/mudaraba"],
  "recommendation": "...",
  "evidence_used": ["chunk_06_rbf_merchant_advance"]
}
```

**Engine Used:** Rule-based (`engine/shariah_engine.py`)
**OpenAI Required:** No

### 7.3 PDF Analysis

```
POST /analyze
Content-Type: multipart/form-data

Request:
file: [PDF file]

Response:
{
  "success": true,
  "filename": "contract.pdf",
  "text_length": 5432,
  "result": {
    "suggestion": "compliant",
    "confidence": 85,
    "summary": "...",
    "issues": [...],
    "reasoning": "...",
    "_metadata": {
      "chunks_used": ["chunk_01_riba_core.md", ...],
      "total_chunks_matched": 3,
      "model_used": "gpt-4o-mini"
    }
  }
}
```

**Engine Used:** OpenAI-powered (`engine/engine.py`)
**OpenAI Required:** Yes (returns error if not configured)

---

## 8. ERROR HANDLING

### 8.1 PDF Upload Errors

- **Invalid file type:** 400 Bad Request
- **Empty file:** 400 Bad Request
- **PDF parsing failure:** 400 Bad Request
- **No text extracted:** 400 Bad Request
- **Analysis failure:** 500 Internal Server Error
- **OpenAI API error:** Returns error in result dict

### 8.2 Structured API Errors

- **Validation error:** 422 Unprocessable Entity (Pydantic)
- **ValueError:** 400 Bad Request
- **Other exceptions:** 500 Internal Server Error

### 8.3 OpenAI Configuration

- **Missing API key:** Engine returns error dict with `verdict="ERROR"`
- **API call failure:** Returns error dict with exception details

---

## 9. CONFIGURATION

### 9.1 Environment Variables

- `OPENAI_API_KEY`: Required for `/analyze` endpoint (optional for `/api/shariah-check`)
- `DEBUG`: Set to "true" for debug logging (default: "false")

### 9.2 OpenAI Client Initialization

**File:** `openai_config.py`

```python
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = AsyncOpenAI(api_key=api_key)
    model = "gpt-4o-mini"
else:
    client = None
    model = None
```

**Behavior:**
- If API key not set: Client is None, `/analyze` returns error
- If API key set: Client initialized, `/analyze` works normally

---

## 10. KEY DIFFERENCES BETWEEN ENGINES

| Feature | Rule-Based Engine | OpenAI Engine |
|---------|------------------|---------------|
| **File** | `engine/shariah_engine.py` | `engine/engine.py` |
| **Endpoint** | `/api/shariah-check` | `/analyze` |
| **Input** | Structured (Pydantic model) | Free-form text |
| **Analysis** | Deterministic rules | LLM (GPT-4o-mini) |
| **OpenAI Required** | No | Yes |
| **RAG Method** | Token overlap scoring | Keyword matching |
| **Response Format** | `ShariaCheckResponse` | Custom dict |
| **Use Case** | Structured product data | PDF documents |

---

## 11. CONNECTING COMPONENTS

### 11.1 How PDF Upload Connects to OpenAI Engine

```
main.py
  ├── Imports: from engine.engine import analyze_shariah_compliance
  ├── Endpoint: @app.post("/analyze")
  ├── PDF parsing: parse_pdf_text(file_bytes) → extracted_text
  └── Calls: await analyze_shariah_compliance(extracted_text)
      ↓
engine/engine.py
  ├── Imports: from openai_config import client, model
  ├── Function: async def analyze_shariah_compliance(text)
  ├── Retrieval: get_chunks(text) → matching_chunks
  ├── Formatting: format_chunks(chunks) → context
  ├── Prompt: Constructs system + user prompts
  └── API Call: await client.chat.completions.create(...)
```

### 11.2 How Structured API Connects to Rule-Based Engine

```
routes/shariah_check.py
  ├── Imports: from services.shariah_engine import check_shariah_compliance
  ├── Endpoint: @router.post("/shariah-check")
  └── Calls: await check_shariah_compliance(request)
      ↓
services/shariah_engine.py
  ├── Imports: from engine.shariah_engine import check_shariah_compliance
  └── Delegates: return await _check_shariah_compliance(request)
      ↓
engine/shariah_engine.py
  ├── Imports: 
  │   ├── from engine.rag_store import load_kb
  │   ├── from engine.retriever import retrieve
  │   └── from engine.llm_reasoner import build_*
  ├── Function: async def check_shariah_compliance(request)
  ├── Processing: Feature extraction → Classification → Checks → Scoring
  ├── RAG: load_kb() → retrieve() → build_*()
  └── Returns: ShariaCheckResponse
```

### 11.3 Shared Components

**Knowledge Base:**
- Both engines read from `data/shariah_kb/*.md`
- Rule-based: Uses `rag_store.load_kb()` (cached)
- OpenAI: Uses `get_chunks()` (direct file reading)

**Keyword Matching:**
- Rule-based: Token overlap (alphanumeric tokens)
- OpenAI: Word boundary regex matching

---

## 12. DATA FLOW DIAGRAMS

### 12.1 Structured API Flow

```
[Client] 
  → POST /api/shariah-check (JSON)
  → [routes/shariah_check.py] (Validation)
  → [services/shariah_engine.py] (Interface)
  → [engine/shariah_engine.py] (Rule-based processing)
    ├── Feature extraction
    ├── Classification
    ├── Compliance checks
    ├── Confidence scoring
    └── RAG integration
      ├── [rag_store.py] (Load KB)
      ├── [retriever.py] (Retrieve chunks)
      └── [llm_reasoner.py] (Enhance output)
  → [ShariaCheckResponse]
  → [Client]
```

### 12.2 PDF Upload Flow

```
[Client]
  → POST /analyze (PDF file)
  → [main.py] (File handling)
    ├── Validate PDF
    ├── Extract text (PyMuPDF)
    └── [engine/engine.py] (OpenAI processing)
      ├── [get_chunks()] (Keyword matching)
      ├── [format_chunks()] (Context formatting)
      ├── [OpenAI API] (LLM analysis)
      └── [Response processing]
  → [JSON Response]
  → [Client]
```

---

## 13. CRITICAL IMPLEMENTATION DETAILS

### 13.1 PDF Text Extraction

**Library:** PyMuPDF (fitz)
**Function:** `parse_pdf_text(file_bytes: bytes) -> str`

```python
pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
for page in pdf_document:
    text = page.get_text()
    text_parts.append(text)
return "\n\n".join(text_parts)
```

**Error Cases:**
- Invalid PDF format
- Encrypted PDF
- Image-only PDF (no text)

### 13.2 Keyword Extraction (OpenAI Engine)

**Function:** `extract_keywords_from_chunk(content: str) -> list[str]`

```python
# Parses "Keywords: keyword1, keyword2, ..." from markdown
p = content.split('Keywords:')
if len(p) > 1:
    words = p[1].split('#')[0].strip()  # Stop at next # (section)
    return words.split(',')
return []
```

### 13.3 Keyword Matching (OpenAI Engine)

**Function:** `get_chunks(text: str) -> list[dict]`

```python
for keyword in keywords:
    pattern = r'\b' + re.escape(keyword) + r'\b'  # Word boundary
    if re.search(pattern, text_lower):
        matched_keywords.append(keyword)
```

**Why word boundaries:** Prevents partial matches (e.g., "interest" in "interesting")

### 13.4 Token Overlap (Rule-Based Engine)

**Function:** `retrieve(query: str, chunks: List[DocChunk], k: int) -> List[DocChunk]`

```python
q_tokens = set(re.findall(r"[a-zA-Z]+", query.lower()))
for chunk in chunks:
    c_tokens = set(re.findall(r"[a-zA-Z]+", chunk.text.lower()))
    score = len(q_tokens.intersection(c_tokens))
    scored.append((score, chunk))
return top_k(scored, k)
```

**Difference from OpenAI engine:** Uses set intersection, not regex matching

---

## 14. TESTING THE SYSTEM

### 14.1 Test Structured API

```bash
curl -X POST http://localhost:8000/api/shariah-check \
  -H "Content-Type: application/json" \
  -d '{
    "product_type": "revenue-based-advance",
    "interest_rate": 0,
    "profit_sharing_pct": 5,
    "terms_length_months": 12,
    "description": "VePay revenue-based advance: $50K advance against 5% of daily seller revenue"
  }'
```

**Expected:** Works without OpenAI API key

### 14.2 Test PDF Upload

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@contract.pdf"
```

**Expected:** Requires OpenAI API key (returns error if not set)

---

## 15. SUMMARY FOR LLM UNDERSTANDING

**Key Points:**

1. **Two Separate Engines:**
   - Rule-based: Deterministic, structured input, no OpenAI
   - OpenAI-powered: LLM analysis, free-form text, requires API key

2. **Two Different RAG Systems:**
   - Rule-based: Token overlap scoring, cached KB loading
   - OpenAI: Keyword regex matching, direct file reading

3. **Two Different Endpoints:**
   - `/api/shariah-check`: Structured JSON input → Rule-based engine
   - `/analyze`: PDF upload → OpenAI engine

4. **Shared Knowledge Base:**
   - Both engines use `data/shariah_kb/*.md` files
   - Different retrieval methods but same source

5. **Component Connections:**
   - `main.py` → `engine/engine.py` (PDF flow)
   - `routes/shariah_check.py` → `services/shariah_engine.py` → `engine/shariah_engine.py` (Structured flow)
   - Both engines independently access knowledge base

6. **Error Handling:**
   - OpenAI engine gracefully handles missing API key
   - Both engines return structured error responses
   - PDF parsing errors are caught and returned as HTTP errors

This architecture allows the system to work with or without OpenAI, providing deterministic analysis for structured data and LLM-powered analysis for documents.

---

**END OF DOCUMENTATION**
