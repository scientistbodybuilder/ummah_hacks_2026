"""Tests for /api/analyze-contract endpoint."""

import pytest
from fastapi.testclient import TestClient
from main import app

# Try to import reportlab for PDF generation, fallback to simple bytes if not available
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def create_test_pdf(text: str = "Test contract with 5% interest rate and late fees.") -> bytes:
    """Create a minimal PDF with text content."""
    if HAS_REPORTLAB:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, text)
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    else:
        # Fallback: return minimal PDF bytes (this is a very basic PDF structure)
        # In production, you'd use reportlab or similar
        # For testing, we'll create a simple text-based PDF
        pdf_content = f"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length {len(text) + 50}
>>
stream
BT
/F1 12 Tf
100 700 Td
({text}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000300 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
400
%%EOF"""
        return pdf_content.encode('latin-1')


client = TestClient(app)


def test_non_pdf_upload():
    """Test that non-PDF upload returns 400."""
    response = client.post(
        "/api/analyze-contract",
        files={"file": ("test.txt", b"not a pdf", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_empty_pdf():
    """Test that empty PDF bytes returns 400."""
    response = client.post(
        "/api/analyze-contract",
        files={"file": ("empty.pdf", b"", "application/pdf")}
    )
    assert response.status_code == 400
    assert "Empty file" in response.json()["detail"]


def test_valid_pdf_with_text():
    """Test that a valid PDF with text returns 200 and has required keys."""
    pdf_bytes = create_test_pdf("This is a loan contract with 5% annual interest rate and late payment fees of $50.")
    
    response = client.post(
        "/api/analyze-contract",
        files={"file": ("test_contract.pdf", pdf_bytes, "application/pdf")}
    )
    
    # Should return 200 even without OpenAI key (verdict will be "uncertain")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check required top-level keys
    assert "success" in data
    assert "filename" in data
    assert "text_length" in data
    assert "verdict" in data
    assert "confidence" in data
    assert "contract_type" in data
    assert "summary" in data
    assert "reasoning" in data
    assert "issues" in data
    assert "missing_info_questions" in data
    assert "evidence_used" in data
    assert "extracted_facts" in data
    assert "_metadata" in data
    
    # Check verdict is one of expected values
    assert data["verdict"] in ["compliant", "non-compliant", "uncertain"]
    
    # Check confidence is in range
    assert 0 <= data["confidence"] <= 100
    
    # Check metadata structure
    metadata = data["_metadata"]
    assert "chunks_considered" in metadata
    assert "chunks_returned" in metadata
    assert "openai_configured" in metadata
    assert "model_used" in metadata or metadata["model_used"] is None
    assert "llm_error" in metadata or metadata["llm_error"] is None
    assert "text_truncated" in metadata
    
    # Check extracted_facts structure
    facts = data["extracted_facts"]
    assert "contract_type_guess" in facts
    assert "repayment_structure" in facts
    assert "interest_or_apr_present" in facts
    assert "quotes" in facts
    
    # If OpenAI not configured, should still work but with uncertain verdict
    if not metadata["openai_configured"]:
        assert data["verdict"] == "uncertain" or data["verdict"] == "non-compliant"
        # Should still have issues if interest detected
        if facts.get("interest_or_apr_present"):
            assert len(data["issues"]) > 0


def test_pdf_with_interest_detection():
    """Test that interest detection works in heuristics mode."""
    pdf_bytes = create_test_pdf(
        "Loan Agreement: Principal $10,000, Annual Percentage Rate (APR) of 8.5% per annum. "
        "Late payment fee of $25 applies after 10 days grace period."
    )
    
    response = client.post(
        "/api/analyze-contract",
        files={"file": ("loan.pdf", pdf_bytes, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should detect interest
    assert data["extracted_facts"]["interest_or_apr_present"] is True
    
    # Should have riba issue
    riba_issues = [i for i in data["issues"] if i["principle"] == "riba"]
    assert len(riba_issues) > 0
    
    # Should have late fee issue
    late_fee_issues = [i for i in data["issues"] if i["principle"] == "late_fees"]
    assert len(late_fee_issues) > 0
