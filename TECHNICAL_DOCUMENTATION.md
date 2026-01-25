# SHARAH MVP: Complete Technical Documentation

**Version:** 1.0  
**Date:** January 24, 2026  
**Status:** Ready for Development  
**Audience:** Developers, AI Assistants (Cursor), Technical Reviewers

---

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Architecture & Design](#architecture--design)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [API Specification](#api-specification)
6. [Frontend Specification](#frontend-specification)
7. [Data & Logic Specification](#data--logic-specification)
8. [Database Schema](#database-schema)
9. [Deployment & DevOps](#deployment--devops)
10. [Testing Strategy](#testing-strategy)
11. [Performance & Optimization](#performance--optimization)
12. [Security Considerations](#security-considerations)
13. [Error Handling](#error-handling)
14. [Development Workflow](#development-workflow)

---

## SYSTEM OVERVIEW

### What is SHARAH?

SHARAH is a real-time Shariah compliance validation API for Islamic financial products. Users submit product specifications (interest rates, profit-sharing terms, payment structures), and SHARAH analyzes them against Islamic finance principles, returning a compliance assessment with confidence score, reasoning, and specific recommendations.

### Core Value Proposition

- **Problem:** Islamic banks spend 3-5 weeks validating new products with Shariah scholars
- **Solution:** SHARAH validates products in <1 second using AI + rule-based logic
- **Impact:** 3-5 week bottleneck → instant validation + scholar review optimization

### High-Level Flow

```
User Input (Product Spec)
    ↓
Frontend Form (Next.js)
    ↓
API Endpoint (FastAPI)
    ↓
Shariah Engine (Rule-based + ML/ready)
    ↓
Response (Compliance + Confidence + Reasoning)
    ↓
Frontend Results Display
    ↓
User Sees: ✅ HALAL (96% confidence) or ❌ HARAM
```

---

## ARCHITECTURE & DESIGN

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     User's Browser                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Frontend (Next.js 14)                       │   │
│  │  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐ │   │
│  │  │ Landing    │  │  Dashboard   │  │  Product Form    │ │   │
│  │  │ Page       │  │  Layout      │  │  + Results       │ │   │
│  │  └────────────┘  └──────────────┘  └──────────────────┘ │   │
│  │           ↓ (HTTPS POST to /api/shariah-check)          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI on Railway)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               main.py (FastAPI App)                     │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │  Middleware: CORS, Auth (future), Logging         │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │           ↓                                            │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │  Routes:                                           │ │   │
│  │  │  - GET /health                                    │ │   │
│  │  │  - POST /api/shariah-check (Main endpoint)        │ │   │
│  │  │  - (Future) POST /api/signup                      │ │   │
│  │  │  - (Future) GET /api/history                      │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │           ↓                                            │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │  Shariah Engine (Core Logic)                       │ │   │
│  │  │  ├─ Rule-based checks                             │ │   │
│  │  │  ├─ Confidence scoring                            │ │   │
│  │  │  ├─ Fatwa mapping                                 │ │   │
│  │  │  ├─ Reasoning generation                          │ │   │
│  │  │  └─ Edge case handling                            │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │           ↓                                            │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │  Data Layer                                        │ │   │
│  │  │  ├─ fatwas_database.json (Shariah rules)          │ │   │
│  │  │  ├─ Pydantic models (request/response schemas)   │ │   │
│  │  │  └─ (Future) Supabase PostgreSQL DB              │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    Response (JSON)
                            ↓
                    Frontend Display
```

### Design Patterns

**1. Separation of Concerns**
- **Frontend:** Presentation + User interaction only
- **Backend:** Business logic + Data processing only
- **Shariah Engine:** Compliance checking logic isolated from API layer

**2. Stateless API**
- No session state required
- Each request is independent
- Easy to scale horizontally

**3. Rule-Based + ML-Ready**
- MVP uses deterministic rules (100% reproducible)
- Architecture allows future ML fine-tuning (OpenAI integration)
- Easy to debug (rules are auditable)

**4. Layered Architecture**
```
Presentation Layer (Frontend)
    ↓
API Layer (FastAPI routes)
    ↓
Business Logic Layer (Shariah engine)
    ↓
Data Layer (Rules database + future DB)
```

---

## TECHNOLOGY STACK

### Frontend

| Component | Technology | Version | Why |
|-----------|-----------|---------|-----|
| Framework | Next.js | 14.x | React + SSR + built-in optimizations |
| Language | JavaScript | ES6+ | Fast iteration, minimal setup |
| Styling | Tailwind CSS | 3.x | Utility-first, consistent design |
| State Management | React Hooks | Built-in | useState, no extra dependencies |
| HTTP Client | Fetch API / Axios | Built-in | Simple API calls |
| Deployment | Vercel | - | Next.js native, auto-deploy on GitHub push |

### Backend

| Component | Technology | Version | Why |
|-----------|-----------|---------|-----|
| Framework | FastAPI | 0.104+ | Async, automatic OpenAPI docs, type-safe |
| Language | Python | 3.9+ | Fast development, great for data/ML |
| Async Runtime | Uvicorn | 0.24+ | ASGI server, handles async operations |
| Validation | Pydantic | 2.x | Type hints + runtime validation |
| Environment | python-dotenv | 1.0+ | .env file support |
| Deployment | Railway | - | Python-native, simple FastAPI deployment |

### Data & Rules

| Component | Format | Purpose |
|-----------|--------|---------|
| Fatwas Database | JSON | Shariah rules, principles, mappings |
| Test Data | JSON | Test products + expected outputs |
| Configuration | .env files | API keys, URLs, environment variables |

### DevOps & Infrastructure

| Component | Service | Purpose |
|-----------|---------|---------|
| Source Control | GitHub | Code repository, deployment hooks |
| Frontend Deploy | Vercel | Next.js hosting, auto-deploy |
| Backend Deploy | Railway | FastAPI hosting, auto-deploy |
| Monitoring | Railway/Vercel Logs | Error tracking, performance monitoring |
| CI/CD | GitHub Actions (future) | Automated testing, deployment |

---

## PROJECT STRUCTURE

### Frontend Structure

```
sharah-frontend/
├── app/                                 # Next.js 14 app directory
│   ├── page.jsx                        # Landing page (home route)
│   ├── layout.jsx                      # Root layout
│   ├── globals.css                     # Global styles
│   ├── dashboard/                      # Dashboard route group
│   │   ├── page.jsx                    # Dashboard shell (main app)
│   │   └── components/
│   │       ├── ProductForm.jsx         # Form component (5 inputs)
│   │       └── ResultsDisplay.jsx      # Results display component
│   └── api/                            # (Future) API routes for auth
│       └── route.js
│
├── public/                             # Static assets
│   ├── logo.png
│   ├── favicon.ico
│   └── images/
│
├── styles/                             # CSS files
│   ├── globals.css
│   └── components.css
│
├── package.json                        # NPM dependencies
├── package-lock.json
├── next.config.js                      # Next.js configuration
├── tailwind.config.js                  # Tailwind configuration
├── .env.local                          # Environment variables (local)
├── .env.example                        # Example env template
├── .gitignore
└── README.md

Total Lines of Code (Frontend):
- app/page.jsx: ~200 lines
- app/dashboard/page.jsx: ~200 lines
- ProductForm.jsx: ~150 lines
- ResultsDisplay.jsx: ~200 lines
- Other (config): ~100 lines
- TOTAL: ~850 lines
```

### Backend Structure

```
sharah-backend/
├── main.py                             # FastAPI app entry point
├── routes/                             # API routes
│   ├── __init__.py
│   └── shariah_check.py               # POST /api/shariah-check endpoint
│
├── services/                           # Business logic
│   ├── __init__.py
│   └── shariah_engine.py              # Core compliance checking
│
├── models/                             # Data models
│   ├── __init__.py
│   └── schemas.py                     # Pydantic request/response schemas
│
├── data/                               # Data files
│   ├── fatwas_database.json           # Shariah rules + principles
│   └── product_examples.json          # Test products
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── test_shariah.py                # Unit tests (20+ test cases)
│   ├── test_api.py                    # Integration tests
│   ├── test_data.json                 # Test fixtures
│   └── conftest.py                    # Pytest configuration
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                # System design details
│   ├── SHARIAH_RULES.md              # Documented Shariah logic
│   ├── API.md                         # API documentation
│   └── TESTING.md                     # Testing guide
│
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (live)
├── .env.example                        # Example env template
├── Dockerfile                          # Docker configuration
├── .gitignore
└── README.md

Total Lines of Code (Backend):
- main.py: ~50 lines
- shariah_engine.py: ~300 lines
- schemas.py: ~80 lines
- shariah_check.py: ~60 lines
- test_shariah.py: ~350 lines
- Other (config): ~100 lines
- TOTAL: ~940 lines
```

---

## API SPECIFICATION

### Endpoint: POST /api/shariah-check

**Description:** Validate Islamic financial product for Shariah compliance

**URL:** `https://sharah-api.railway.app/api/shariah-check` (production) or `http://localhost:8000/api/shariah-check` (local)

**Method:** POST

**Content-Type:** application/json

#### Request Schema

```python
class ShariaCheckRequest(BaseModel):
    product_type: str              # Required: "revenue-based-advance", "musharaka", "murabahah", "sukuk", "bnpl", "other"
    interest_rate: float           # Required: 0-50 (annual %, e.g., 5.5)
    profit_sharing_pct: float      # Required: 0-50 (%, e.g., 7.5)
    terms_length_months: int       # Required: 1-120 (duration of agreement)
    description: str               # Required: Plain text product description
```

#### Request Example

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

#### Response Schema

```python
class ShariaCheckResponse(BaseModel):
    is_shariah_compliant: bool              # true if Halal, false if Haram
    confidence: float                       # 0-100% confidence in assessment
    reasoning: str                          # Explanation of why Halal/Haram
    flagged_issues: List[str]              # Specific issues found (empty if compliant)
    applicable_fatwas: List[str]           # Islamic principles that apply
    recommendation: str                     # Next step for user
```

#### Response Example (Halal)

```json
{
  "is_shariah_compliant": true,
  "confidence": 96,
  "reasoning": "Product uses revenue-based advance structure with profit-sharing. No fixed interest (Riba). Risk is shared between lender and borrower (Musharaka principles apply). All terms are transparent.",
  "flagged_issues": [],
  "applicable_fatwas": [
    "musharaka",
    "profit-sharing",
    "risk-sharing"
  ],
  "recommendation": "Compliant. Ready for launch. Can be presented to Shariah board with high confidence."
}
```

#### Response Example (Haram)

```json
{
  "is_shariah_compliant": false,
  "confidence": 15,
  "reasoning": "Fixed interest rate of 5% detected. This violates Riba prohibition - charging interest on money is Haram in Islamic finance.",
  "flagged_issues": [
    "Fixed interest rate (Riba prohibited)",
    "No profit-sharing to offset interest"
  ],
  "applicable_fatwas": [
    "riba"
  ],
  "recommendation": "Not compliant. Redesign product: Remove fixed interest OR restructure as profit-sharing model (Musharaka/Murabahah)."
}
```

#### Response Example (Medium Confidence)

```json
{
  "is_shariah_compliant": true,
  "confidence": 78,
  "reasoning": "Product structure is likely Shariah-compliant, but contains uncertain terms regarding penalty fees. Gharar (excessive uncertainty) detected in one clause.",
  "flagged_issues": [
    "Gharar detected in penalty fee clause - terms could be clearer"
  ],
  "applicable_fatwas": [
    "musharaka",
    "gharar"
  ],
  "recommendation": "Likely compliant, but recommend Shariah scholar review the flagged clause specifically. Clarify penalty fee structure to reduce Gharar."
}
```

### Error Responses

#### 400 Bad Request

```json
{
  "detail": [
    {
      "loc": ["body", "interest_rate"],
      "msg": "ensure this value is less than 50",
      "type": "value_error.number.not_less_than"
    }
  ]
}
```

#### 500 Internal Server Error

```json
{
  "detail": "Internal server error processing request"
}
```

### Response Status Codes

- `200 OK` - Validation successful
- `400 Bad Request` - Invalid input (missing fields, wrong type, out of range)
- `422 Unprocessable Entity` - Validation error (Pydantic)
- `500 Internal Server Error` - Backend error
- `503 Service Unavailable` - Server overloaded

### Performance Requirements

- Response time: <1 second (target: <500ms)
- Concurrent requests: Handle 100+ simultaneous requests
- Uptime: 99.9% (monitored on Railway)

### Rate Limiting (Future)

```
- No rate limiting in MVP
- Post-MVP: 100 requests per minute per user
```

### Authentication (Future)

```
- No auth in MVP
- Post-MVP: JWT token-based auth via Supabase
```

---

## FRONTEND SPECIFICATION

### Page: Landing (/)

**File:** `app/page.jsx`

**Components:**
1. **Hero Section**
   - Headline: "SHARAH: Instant Shariah Compliance"
   - Subheadline: "Validate Islamic financial products in seconds, not weeks."
   - CTA Button: "Try SHARAH Now" → Links to /dashboard
   - Background: Linear gradient (dark theme)

2. **Features Section**
   - 3 feature cards displayed in grid (3 cols on desktop, 1 col on mobile)
   - Card 1: ⚡ Instant - "Validate products in <1 second, not 3-5 weeks"
   - Card 2: 🎯 Accurate - "98% F1 score on Shariah compliance vs 60% for generic AI"
   - Card 3: 📊 Transparent - "See which fatwas were checked, full audit trail"

3. **Video Section**
   - Embedded video (Loom placeholder)
   - 60-90 seconds showing product in action
   - Shows: Form submission → Loading → Results display

4. **Footer CTA**
   - "Ready to validate faster?" + Call to action button

**Styling:**
- Dark theme: Backgrounds (slate-900, slate-800), Text (white, slate-200)
- Accent color: Teal-500 for buttons
- Responsive: Stacked on mobile, grid on desktop
- Font: System fonts (efficient, fast)

**Performance:**
- Page load: <2 seconds
- Images: Optimized, lazy-loaded
- No external dependencies (minimal JS)

---

### Page: Dashboard (/dashboard)

**File:** `app/dashboard/page.jsx`

**State Management:**
```javascript
const [formData, setFormData] = useState({
  product_type: "revenue-based-advance",
  interest_rate: 0,
  profit_sharing_pct: 0,
  terms_length_months: 12,
  description: ""
})

const [result, setResult] = useState(null)      // API response
const [loading, setLoading] = useState(false)   // Loading state
const [error, setError] = useState(null)        // Error state
```

**Layout:**
- Form on left (desktop) or top (mobile)
- Results on right (desktop) or bottom (mobile)
- Responsive breakpoint: 768px (md in Tailwind)

**Form Submission Flow:**
1. User fills 5 fields
2. Form validates required fields
3. User clicks "Check Compliance"
4. Loading state = true, spinner shown
5. POST to API: `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/shariah-check`
6. API returns response
7. Display results: `setResult(response.data)`
8. Loading state = false

---

### Component: ProductForm

**File:** `app/dashboard/components/ProductForm.jsx`

**Props:**
```javascript
{
  formData: object,           // Form values
  onFormChange: function,     // onChange handler
  onSubmit: function,         // onSubmit handler
  loading: boolean            // Disable during API call
}
```

**Fields:**

1. **Product Type** (Dropdown)
   - Options: revenue-based-advance, musharaka, murabahah, sukuk, bnpl, other
   - Default: revenue-based-advance
   - Required: Yes

2. **Interest Rate** (Number Input)
   - Min: 0, Max: 50, Step: 0.1
   - Placeholder: "0.0"
   - Unit: % (annual)
   - Required: Yes

3. **Profit Sharing %** (Number Input)
   - Min: 0, Max: 50, Step: 0.1
   - Placeholder: "0.0"
   - Unit: %
   - Required: Yes

4. **Terms Length** (Number Input)
   - Min: 1, Max: 120, Step: 1
   - Placeholder: "12"
   - Unit: months
   - Required: Yes

5. **Description** (Textarea)
   - Rows: 5
   - Placeholder: "Describe your product structure..."
   - Required: Yes

**Submit Button:**
- Text: "Check Compliance"
- Disabled during loading (loading = true)
- Styling: Teal-500 background, white text, rounded

**Validation:**
- All fields required
- Interest rate: 0-50
- Profit sharing: 0-50
- Terms: 1-120

---

### Component: ResultsDisplay

**File:** `app/dashboard/components/ResultsDisplay.jsx`

**Props:**
```javascript
{
  result: object              // API response
}
```

**Conditional Rendering:**
- Show only if result != null

**Layout:**

1. **Header**
   - Icon: ✅ if compliant, ❌ if not
   - Title: "Shariah Compliant" (green) or "Not Compliant" (red)
   - Confidence: "Confidence: 96%"

2. **Reasoning Section**
   - Heading: "Reasoning"
   - Text: result.reasoning (multiline, readable)

3. **Flagged Issues Section** (conditional - only if flagged_issues.length > 0)
   - Heading: "⚠️ Flagged Issues"
   - List: result.flagged_issues as bullet points

4. **Applicable Fatwas Section** (conditional - only if applicable_fatwas.length > 0)
   - Heading: "📜 Applicable Fatwas"
   - List: result.applicable_fatwas as bullet points

5. **Recommendation Section**
   - Heading: "Recommendation"
   - Text: result.recommendation (in highlighted box)

**Styling:**
- Background: Green (green-900) if compliant, Red (red-900) if not
- Text: White, readable on colored background
- Spacing: Proper padding + margins

**Features:**
- Copy to clipboard button (future)
- Download as JSON (future)
- Share results link (future)

---

## DATA & LOGIC SPECIFICATION

### Shariah Engine

**File:** `backend/services/shariah_engine.py`

**Function Signature:**
```python
async def check_shariah_compliance(request: ShariaCheckRequest) -> ShariaCheckResponse
```

### Rule-Based Logic

#### Rule 1: Interest Detection (Riba)

```
IF interest_rate > 0 AND profit_sharing_pct == 0:
  → is_shariah_compliant = false
  → confidence = 15-30% (very low)
  → flagged_issue = "Fixed interest rate (Riba prohibited)"
  → applicable_fatwa = "riba"
  → reasoning = "Fixed interest on money is Haram"

IF interest_rate > 0 AND profit_sharing_pct > 0:
  → Check profit-sharing adequacy
  → IF profit_sharing_pct >= interest_rate:
    → Potentially Halal (offset interest with profit-sharing)
    → confidence = 60-75%
  → ELSE:
    → Flag: "Profit-sharing may not offset interest"
    → confidence = 40-60%
```

#### Rule 2: Profit-Sharing (Musharaka)

```
IF interest_rate == 0 AND profit_sharing_pct > 0:
  → is_shariah_compliant = true (likely)
  → confidence = 80-98% (depending on product type)
  → applicable_fatwa = "musharaka", "profit-sharing"
  → reasoning = "Matches Musharaka profit-sharing principles"
```

#### Rule 3: Zero Terms (Require Product Type Analysis)

```
IF interest_rate == 0 AND profit_sharing_pct == 0:
  → Depends on product_type
  → IF product_type == "murabahah":
    → Could be cost-plus markup
    → confidence = 70-85%
  → ELSE:
    → Inconclusive (need more info)
    → confidence = 50-60%
    → recommendation = "Provide more details about pricing structure"
```

#### Rule 4: Gharar Detection (Excessive Uncertainty)

```
IF product description is vague or unclear:
  → Flag: "Gharar detected - terms could be clearer"
  → Subtract 10-20% from confidence
  → applicable_fatwa = "gharar"

IF payment schedule is undefined:
  → Flag: "Payment terms unclear"
  → confidence reduction = 15%
```

### Confidence Scoring Algorithm

```python
def calculate_confidence(interest_rate, profit_sharing_pct, flagged_issues):
    base_confidence = 50  # Start at 50%
    
    # Add points for positive signals
    if interest_rate == 0:
        base_confidence += 20  # No interest is good
    
    if profit_sharing_pct > 0:
        base_confidence += min(profit_sharing_pct * 2, 30)  # Add 2% per % profit share (max +30%)
    
    if interest_rate > 0 and profit_sharing_pct >= interest_rate:
        base_confidence += 10  # Profit-sharing offsets interest
    
    # Subtract points for issues
    base_confidence -= len(flagged_issues) * 5  # -5% per issue
    
    # Cap at 0-100
    confidence = max(0, min(100, base_confidence))
    
    return confidence
```

### Fatwa Mapping

```python
FATWA_MAP = {
    "riba": "Interest on money (Prohibited)",
    "musharaka": "Profit-sharing partnership (Permitted)",
    "murabahah": "Cost-plus markup sale (Permitted)",
    "gharar": "Excessive uncertainty (Prohibited)",
    "profit-sharing": "Revenue/profit sharing (Permitted)",
    "risk-sharing": "Shared risk between parties (Permitted)",
    "asset-backed": "Backed by real assets (Permitted)"
}

def map_fatwas(interest_rate, profit_sharing_pct, product_type, issues):
    fatwas = []
    
    if interest_rate > 0:
        fatwas.append("riba")
    
    if profit_sharing_pct > 0:
        fatwas.append("musharaka")
        fatwas.append("profit-sharing")
    
    if product_type == "murabahah":
        fatwas.append("murabahah")
    
    if any("unclear" in issue.lower() for issue in issues):
        fatwas.append("gharar")
    
    # Remove duplicates
    return list(set(fatwas))
```

### Reasoning Generation

```python
def generate_reasoning(is_compliant, interest_rate, profit_sharing_pct, 
                       product_type, applicable_fatwas):
    
    reasoning = f"Product uses {product_type} structure "
    
    if interest_rate == 0:
        reasoning += "with no fixed interest (Riba-free). "
    else:
        reasoning += f"with {interest_rate}% interest rate. "
    
    if profit_sharing_pct > 0:
        reasoning += f"Includes {profit_sharing_pct}% profit-sharing. "
    
    if "musharaka" in applicable_fatwas:
        reasoning += "Follows Musharaka (partnership) principles where both parties share profit and loss. "
    
    if "riba" in applicable_fatwas:
        reasoning += "Contains Riba (interest), which is prohibited in Islamic finance. "
    
    if is_compliant:
        reasoning += "Overall: Shariah-compliant."
    else:
        reasoning += "Overall: NOT Shariah-compliant."
    
    return reasoning
```

---

## DATABASE SCHEMA

### MVP (No Database)

In MVP, all data is static JSON files in `backend/data/`:

#### fatwas_database.json

```json
{
  "principles": {
    "riba": {
      "name": "Riba (Interest)",
      "definition": "Charging interest on money or loans",
      "status": "Haram (Prohibited)",
      "reference": "Quran 2:275-2:276, AAOIFI FAS 1"
    },
    "musharaka": {
      "name": "Musharaka (Partnership)",
      "definition": "Partnership where both parties share profit and loss",
      "status": "Halal (Permitted)",
      "reference": "AAOIFI FAS 12"
    },
    "murabahah": {
      "name": "Murabahah (Cost-Plus)",
      "definition": "Sale with transparent markup on cost",
      "status": "Halal (Permitted)",
      "reference": "AAOIFI FAS 2"
    },
    "gharar": {
      "name": "Gharar (Uncertainty)",
      "definition": "Excessive uncertainty or ambiguity in terms",
      "status": "Haram (Prohibited)",
      "reference": "Hadith collections"
    }
  },
  "rules": [
    {
      "id": "RIBA_001",
      "description": "Fixed interest rate on money",
      "condition": "interest_rate > 0 AND profit_sharing_pct == 0",
      "verdict": "Haram",
      "confidence_adjustment": -30,
      "flag": "Fixed interest rate (Riba prohibited)"
    },
    {
      "id": "MUSHARAKA_001",
      "description": "Profit-sharing partnership",
      "condition": "interest_rate == 0 AND profit_sharing_pct > 0",
      "verdict": "Halal",
      "confidence_adjustment": +25,
      "applicable_fatwa": "musharaka"
    }
  ]
}
```

### Post-MVP (Planned)

#### Users Table (Supabase)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  subscription_tier VARCHAR(50)  -- free, pro, enterprise
);
```

#### Compliance Checks Table

```sql
CREATE TABLE compliance_checks (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  product_type VARCHAR(100),
  interest_rate FLOAT,
  profit_sharing_pct FLOAT,
  terms_length_months INT,
  description TEXT,
  result_compliant BOOLEAN,
  result_confidence FLOAT,
  result_reasoning TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## DEPLOYMENT & DEVOPS

### Frontend Deployment (Vercel)

**Setup:**
1. GitHub repo created and pushed
2. Vercel account created
3. Connect GitHub repo to Vercel
4. Environment variables set:
   - `NEXT_PUBLIC_BACKEND_URL=https://sharah-api.railway.app`
5. Deploy with `vercel deploy` or auto-deploy on GitHub push

**Live URL:** `https://sharah-frontend.vercel.app` (example)

**Health Check:**
- Load landing page: Should display in <2 seconds
- Navigation to /dashboard: Should work
- API calls: Should return results

**Monitoring:**
- Vercel dashboard shows deployment status
- Error logs available in Vercel UI
- Performance metrics in Vercel Analytics

### Backend Deployment (Railway)

**Setup:**
1. Railway account created
2. GitHub repo connected to Railway
3. Environment variables set:
   ```
   OPENAI_API_KEY=sk-... (for future LLM integration)
   ENVIRONMENT=production
   ```
4. Deploy with `railway up` or auto-deploy on GitHub push

**Live URL:** `https://sharah-api.railway.app` (example)

**Health Check:**
- GET /health should return 200 OK
- POST /api/shariah-check should respond <1 second
- Test with: `curl https://sharah-api.railway.app/health`

**Monitoring:**
- Railway dashboard shows deployment status
- Logs available in Railway UI
- Auto-scaling configured

### Environment Variables

**.env.example (Backend)**
```
OPENAI_API_KEY=sk-...           # For future AI integration
ENVIRONMENT=development          # or production
DEBUG=true                       # Enable debug logging
DATABASE_URL=...                 # For future Supabase
```

**.env.local (Frontend)**
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000    # Local
# or
NEXT_PUBLIC_BACKEND_URL=https://sharah-api.railway.app  # Production
```

### CI/CD (Future)

GitHub Actions workflow:
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: vercel --prod
      - name: Deploy to Railway
        run: railway up
```

---

## TESTING STRATEGY

### Unit Tests (Backend)

**File:** `backend/tests/test_shariah.py`

**Framework:** pytest

**Test Cases (20+):**

1. Happy Path (Halal)
   - Revenue-based advance (0% int, 5% profit) → ✅ Halal, 96%
   - Musharaka (0% int, 50% profit) → ✅ Halal, 98%
   - Murabahah (0% int, 10% markup) → ✅ Halal, 90%

2. Unhappy Path (Haram)
   - Traditional loan (5% int, 0% profit) → ❌ Haram, 15%
   - Fixed rate savings (3% int, 0% profit) → ❌ Haram, 20%

3. Medium Confidence
   - Complex hybrid → ⚠️ 75% confidence
   - Uncertain terms → ⚠️ 60% confidence

4. Edge Cases
   - Zero interest, zero profit → Depends on type
   - Very high profit share (95%) → Analysis required
   - Negative interest (rebate) → Check separately

**Run Tests:**
```bash
cd backend
pytest tests/test_shariah.py -v
# Output: 20 passed in 0.5s
```

### Integration Tests (Full Stack)

**File:** `backend/tests/test_api.py` + Manual testing

**Tests:**
1. Health endpoint: GET /health → 200 OK
2. API submission: POST /api/shariah-check → Returns valid response
3. Error handling: Invalid input → 400 Bad Request
4. Performance: Response time <1 second
5. CORS headers: Present in response

**Run Tests:**
```bash
cd backend
pytest tests/test_api.py -v
```

### End-to-End Tests (Frontend)

**Manual Testing:**
1. Landing page loads
2. Click "Try SHARAH Now"
3. Fill form with test data
4. Submit form
5. See loading spinner
6. See results appear
7. Verify results match API response

**Browsers Tested:**
- Chrome (latest)
- Firefox (latest)
- Safari (latest)

**Devices Tested:**
- iPhone 12 (375px)
- iPad (768px)
- Desktop (1920px)

### Performance Testing

**Metrics:**
- Backend API response time: <1 second
- Frontend page load: <2 seconds
- Frontend form submission: <3 seconds (including API call)

**Tools:**
- Postman: API load testing
- Lighthouse: Frontend performance
- Railway: Backend monitoring

---

## PERFORMANCE & OPTIMIZATION

### Backend Optimization

**1. Async Operations**
- All endpoints use `async def`
- Non-blocking I/O with FastAPI
- Uvicorn handles multiple concurrent requests

**2. Computation Complexity**
- Shariah engine: O(1) time complexity (simple rule checks)
- No loops over large datasets
- Direct dictionary/list lookups

**3. Response Size**
- JSON response: ~500 bytes typical
- Minimal data transfer
- No unnecessary fields

**4. Caching (Future)**
- Cache common product types
- Cache Shariah rules (rarely change)
- Redis or in-memory cache

### Frontend Optimization

**1. Code Splitting**
- Landing page separate from dashboard
- Components lazy-loaded
- Next.js handles optimization

**2. Bundle Size**
- Minimal dependencies
- Tailwind CSS tree-shaken (only used styles)
- No external libraries (use native Fetch API)

**3. Image Optimization**
- Next.js Image component (automatic optimization)
- Lazy loading for offscreen images
- Responsive images

**4. Rendering Optimization**
- React.memo for components (if needed)
- useCallback for handlers (if needed)
- Avoid unnecessary re-renders

### Database Optimization (Post-MVP)

**1. Indexing**
- Index on `user_id` (for queries)
- Index on `created_at` (for sorting)

**2. Pagination**
- Limit queries to 50 results
- Implement "load more" pattern

**3. Query Optimization**
- SELECT only needed columns
- Use WHERE clauses to filter early

---

## SECURITY CONSIDERATIONS

### Input Validation

**Frontend:**
- Required field validation
- Type checking (number inputs)
- Max length validation (description)

**Backend (Pydantic):**
```python
class ShariaCheckRequest(BaseModel):
    product_type: str = Field(..., min_length=1, max_length=50)
    interest_rate: float = Field(..., ge=0, le=50)
    profit_sharing_pct: float = Field(..., ge=0, le=50)
    terms_length_months: int = Field(..., ge=1, le=120)
    description: str = Field(..., min_length=10, max_length=5000)
```

### SQL Injection Prevention

- POST-MVP: Use parameterized queries
- Avoid string concatenation in SQL
- Use Supabase/ORM for database access

### CORS Security

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sharah.vercel.app"],  # Specific origin in production
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Data Privacy

- No sensitive user data in MVP
- POST-MVP: Encrypt data at rest
- HTTPS only (enforced by Vercel/Railway)
- GDPR compliance (future)

### API Rate Limiting (Future)

```python
# POST-MVP: Limit to 100 requests/minute per user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/shariah-check")
@limiter.limit("100/minute")
async def shariah_check(request: ShariaCheckRequest):
    ...
```

### Authentication (Future)

```python
# POST-MVP: JWT token validation
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/shariah-check")
async def shariah_check(request: ShariaCheckRequest, credentials = Depends(security)):
    # Verify JWT token
    ...
```

---

## ERROR HANDLING

### Frontend Error Handling

```javascript
// In ProductForm component
const handleSubmit = async (e) => {
  e.preventDefault()
  
  try {
    setLoading(true)
    setError(null)
    
    const response = await fetch(`${BACKEND_URL}/api/shariah-check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    })
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    
    const data = await response.json()
    setResult(data)
    
  } catch (err) {
    setError(err.message || "Something went wrong. Please try again.")
  } finally {
    setLoading(false)
  }
}
```

### Backend Error Handling

```python
@app.post("/api/shariah-check")
async def shariah_check(request: ShariaCheckRequest):
    try:
        # Validate input (Pydantic handles this)
        
        # Call Shariah engine
        result = await check_shariah_compliance(request)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### User-Friendly Error Messages

| Error | Message | Action |
|-------|---------|--------|
| Network error | "Connection failed. Check your internet." | Retry button |
| API down | "Service temporarily unavailable. Try again later." | Retry button |
| Invalid input | "Please check your input and try again." | Show field errors |
| Server error | "Something went wrong. Please try again." | Retry button |

---

## DEVELOPMENT WORKFLOW

### Local Development Setup

**Backend:**
```bash
# Clone repo
git clone <repo-url>
cd sharah-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run server
uvicorn main:app --reload

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Frontend:**
```bash
# Clone repo (same or different)
git clone <repo-url>
cd sharah-frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local

# Run dev server
npm run dev

# Site runs at http://localhost:3000
```

### Git Workflow

**Branch Strategy:**
```
main (production) ← PR from develop
develop (staging) ← PR from feature branches
feature/* (work in progress)
```

**Commit Convention:**
```
[Backend] Feature: Add Shariah engine
[Frontend] Fix: Mobile responsive layout
[Docs] Update API specification
```

### Code Review Checklist

Before merge:
- [ ] Code passes lint (no errors)
- [ ] Tests passing (100% pass rate)
- [ ] No console errors
- [ ] Comments explain complex logic
- [ ] PR description explains changes
- [ ] Meets acceptance criteria

---

## APPENDIX: KEY FILES QUICK REFERENCE

| File | Purpose | Owner | Size |
|------|---------|-------|------|
| backend/main.py | FastAPI app setup | Tech Lead | ~50 lines |
| backend/services/shariah_engine.py | Shariah logic | Data Lead | ~300 lines |
| backend/tests/test_shariah.py | Unit tests | Data Lead | ~350 lines |
| frontend/app/page.jsx | Landing page | Frontend | ~200 lines |
| frontend/app/dashboard/page.jsx | Dashboard | Frontend | ~200 lines |
| docs/API.md | API documentation | Support | ~150 lines |
| docs/SHARIAH_RULES.md | Shariah rules | Data Lead | ~200 lines |

---

## SUMMARY: What This Product Does

```
INPUT: Product specification (form with 5 fields)
PROCESSING: Rule-based Shariah compliance engine
OUTPUT: Compliance assessment (✅/❌) with confidence + reasoning
IMPACT: 3-5 week manual review → <1 second instant validation
```

**End-to-end:** User visits website → Fills form → Submits → Gets instant Shariah compliance assessment with confidence score and specific recommendations.

**Technical Stack:** Next.js (frontend) + FastAPI (backend) + Rule-based engine (Shariah logic) + Railway + Vercel (deployment)

**Quality Metrics:** <1s response time, 90%+ accuracy, zero critical bugs, complete documentation

This documentation provides everything needed for developers to build, test, deploy, and maintain SHARAH MVP.