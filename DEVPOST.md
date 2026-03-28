# SHARAH - Instant Shariah Compliance Validation

> **Validate Islamic financial products in seconds, not weeks.**

---

## Inspiration

The Islamic finance industry faces a critical bottleneck: **validating new financial products for Shariah compliance typically takes 3-5 weeks** when reviewed by Shariah scholars. This lengthy process:

- Slows down product launches
- Increases costs for Islamic financial institutions
- Creates friction for fintech innovation in the Muslim world

We recognized an opportunity to leverage **AI and rule-based systems** to provide instant preliminary compliance validation—helping banks and fintech companies accelerate their product development while maintaining Islamic financial principles.

---

## What it does

**SHARAH** is a Shariah compliance validation API for Islamic financial products. Users upload PDF documents or submit product specifications, and SHARAH analyzes them against Islamic finance principles in real-time.

### Key Features

| Feature | Description |
|---------|-------------|
| **Instant Analysis** | Validates products in <1 second |
| **Compliance Verdict** | Clear result: Compliant / Non-Compliant / Uncertain |
| **Confidence Score** | 0-100% confidence in the assessment |
| **Detailed Reasoning** | Explains *why* a product is Halal or Haram |
| **Issue Detection** | Identifies violations like Riba, Gharar, problematic late fees |
| **Evidence Citations** | References Shariah principles and fatwas used |
| **Recommendations** | Actionable next steps for redesign or scholar review |

### Example Output

```
Verdict: NON-COMPLIANT
Confidence: 85%

Issues Found:
  - Riba risk: loan-like structure with interest/return on money

Applicable Principles:
  - riba, late-fees

Recommendation:
  Remove interest-on-loan mechanics or restructure as 
  sale/partnership with proper risk-sharing.
```

---

## How we built it

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React/Vite)                  │
│         - PDF Upload (drag & drop)                       │
│         - Results Display with confidence bars           │
│         - Modern dark theme UI                           │
└────────────────────────┬────────────────────────────────┘
                         │ POST /api/shariah-check
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 Backend (FastAPI/Python)                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Shariah Engine                        │  │
│  │  - Feature Extraction (keyword detection)         │  │
│  │  - Contract Classification                        │  │
│  │  - Compliance Checks (Riba, Gharar, etc.)        │  │
│  │  - Confidence Scoring                             │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │              RAG System                            │  │
│  │  - Knowledge Base (12 Shariah chunks)             │  │
│  │  - Retriever (keyword matching)                   │  │
│  │  - Reasoner (evidence citation)                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

**Backend:**
- Python 3.13+ / FastAPI / Uvicorn
- Pydantic for validation
- Custom RAG implementation

**Frontend:**
- React + Vite
- TailwindCSS
- Drag-and-drop PDF upload

**Knowledge Base:**
- 12 Markdown documents covering Islamic finance principles
- Sourced from AAOIFI standards, Quranic verses, IFSB guidelines

### Shariah Principles Covered

| Principle | Description |
|-----------|-------------|
| **Riba** | Interest prohibition on loans |
| **Gharar** | Excessive uncertainty in contracts |
| **Murabaha** | Cost-plus sale (permitted) |
| **Musharaka** | Equity partnership (permitted) |
| **Mudaraba** | Profit-sharing partnership (permitted) |
| **Ta'widh** | Late fee regulations |
| **Maysir** | Gambling/speculation prohibition |

---

## Challenges we ran into

### 1. Encoding Complex Shariah Rules
Translating nuanced Islamic finance principles into deterministic rule-based logic while maintaining accuracy. Many Shariah rulings have edge cases requiring scholarly interpretation.

### 2. Contract Classification
Distinguishing between:
- **Loan-like structures** (Haram if interest-based)
- **Legitimate profit-sharing** (Halal)
- **Asset-backed sales** (Halal if properly structured)

### 3. Confidence Calibration
Determining appropriate confidence scores that reflect both:
- Clarity of the product structure
- Severity of potential violations

### 4. Handling Ambiguity
Products with vague terms (Gharar) or missing information needed special handling to avoid false positives/negatives.

### 5. Building the Knowledge Base
Curating accurate, cited Shariah rulings from authoritative sources:
- AAOIFI Shariah Standards
- Quranic verses (2:275-276)
- OIC Fiqh Academy rulings
- IFSB Core Principles

---

## Accomplishments that we're proud of

- **Functional Compliance Engine** — Correctly identifies Riba violations, Gharar risks, and partnership compliance issues

- **Comprehensive Knowledge Base** — 12 detailed chunks covering major Islamic finance principles with proper citations

- **RAG Integration** — Evidence-backed reasoning in every compliance assessment

- **Clean Architecture** — Proper separation of concerns (API → Service → Engine → Data layers)

- **Modern UI/UX** — Intuitive drag-and-drop interface with real-time feedback

- **Speed** — <1 second response times for compliance validation

---

## What we learned

### Islamic Finance Fundamentals
- **Riba**: Any premium charged on money loans is strictly Haram
- **Gharar**: Excessive uncertainty invalidates contracts
- **Musharaka/Mudaraba**: Profit-and-loss sharing partnerships are permitted
- **Murabaha**: Cost-plus sales are permitted when properly structured

### Technical Insights
- **Rule-based vs ML**: For compliance systems, deterministic logic provides transparency and auditability that black-box ML cannot match
- **RAG Architecture**: Effective retrieval with clear upgrade paths
- **Domain Knowledge Encoding**: Authoritative sources (AAOIFI, IFSB) are critical for domain-specific AI

---

## What's next for SHARAH

| Priority | Feature | Description |
|----------|---------|-------------|
| **1** | LLM Integration | Semantic embeddings for nuanced document analysis |
| **2** | Enhanced PDF Parsing | Better OCR and structured extraction |
| **3** | Arabic Support | Process original Shariah texts |
| **4** | Scholar Dashboard | Review workflow for Shariah scholars |
| **5** | Fatwa Database | Integration with real fatwa repositories |
| **6** | Enterprise API | For Islamic banks to integrate into pipelines |
| **7** | Continuous Learning | Scholar feedback improves the engine |

---

## Team

Built with dedication at **Ummah Hacks 2026**

---

## Links

- **Demo**: [Try SHARAH](http://localhost:5173)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

> *"Allah has permitted trade and forbidden interest (riba)."*  
> — Quran 2:275
