"""Extract structured facts from contract text."""

from __future__ import annotations

import re
import json
from typing import Literal, Optional, List
from pydantic import BaseModel, Field
from openai_config import client, model


class Quote(BaseModel):
    """A quote from the contract text supporting a fact."""
    field: str
    quote: str


class ContractFacts(BaseModel):
    """Extracted facts from a contract."""
    contract_type_guess: Literal["loan", "murabaha", "mudaraba", "musharaka", "ijara", "wakala", "unknown"] = "unknown"
    repayment_structure: Literal["fixed_installments", "revenue_share", "cost_plus_sale", "unknown"] = "unknown"
    interest_or_apr_present: bool = False
    interest_rate: Optional[float] = None
    late_fee_present: bool = False
    late_fee_description: Optional[str] = None
    guaranteed_return_present: bool = False
    asset_backing_present: Optional[bool] = None
    profit_sharing_present: bool = False
    ambiguity_flags: List[str] = Field(default_factory=list)
    missing_info_questions: List[str] = Field(default_factory=list)
    quotes: List[Quote] = Field(default_factory=list)


def _extract_quotes_for_pattern(text: str, pattern: re.Pattern, field_name: str, context_chars: int = 100) -> List[Quote]:
    """Extract quotes matching a pattern with context."""
    quotes: List[Quote] = []
    matches = pattern.finditer(text)
    
    for match in matches:
        start = max(0, match.start() - context_chars)
        end = min(len(text), match.end() + context_chars)
        quote_text = text[start:end].strip()
        quotes.append(Quote(field=field_name, quote=quote_text))
    
    return quotes


async def extract_contract_facts(text: str) -> ContractFacts:
    """
    Extract structured facts from contract text.
    Uses OpenAI if available, otherwise falls back to heuristics.
    """
    if client is not None and model is not None:
        return await _extract_facts_with_llm(text)
    else:
        return _extract_facts_with_heuristics(text)


async def _extract_facts_with_llm(text: str) -> ContractFacts:
    """Extract facts using OpenAI."""
    system_prompt = """You are a contract analyzer. Extract ONLY facts present in the provided text.
If a fact is not mentioned or unclear, set it to null/false/unknown and add a question to missing_info_questions.
For critical fields (interest/APR, late fee, guaranteed return, markup, asset), provide quotes from the text.

Return JSON with this exact structure:
{
  "contract_type_guess": "loan|murabaha|mudaraba|musharaka|ijara|wakala|unknown",
  "repayment_structure": "fixed_installments|revenue_share|cost_plus_sale|unknown",
  "interest_or_apr_present": true|false,
  "interest_rate": <number|null>,
  "late_fee_present": true|false,
  "late_fee_description": "<string|null>",
  "guaranteed_return_present": true|false,
  "asset_backing_present": true|false|null,
  "profit_sharing_present": true|false,
  "ambiguity_flags": ["<string>"],
  "missing_info_questions": ["<string>"],
  "quotes": [{"field": "<field_name>", "quote": "<exact quote from text>"}]
}"""

    user_prompt = f"""Extract facts from this contract text:

{text[:20000]}  # Cap at 20k chars

Provide quotes for any detected: interest/APR, late fee, guaranteed return, markup, asset mentions."""

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result_text = response.choices[0].message.content
        facts_dict = json.loads(result_text)
        
        # Convert quotes to Quote objects
        quotes_raw = facts_dict.get("quotes", [])
        quotes = []
        for q in quotes_raw:
            if isinstance(q, dict):
                quotes.append(Quote(**q))
            elif isinstance(q, Quote):
                quotes.append(q)
        facts_dict["quotes"] = quotes
        
        return ContractFacts(**facts_dict)
        
    except Exception as e:
        # Fallback to heuristics on LLM error
        return _extract_facts_with_heuristics(text)


def _extract_facts_with_heuristics(text: str) -> ContractFacts:
    """Extract facts using regex heuristics."""
    text_lower = text.lower()
    facts = ContractFacts()
    quotes: List[Quote] = []
    
    # Interest/APR detection
    interest_patterns = [
        r'\b(?:apr|annual percentage rate|interest rate|interest|% per annum|% p\.?a\.?)\s*:?\s*(\d+\.?\d*)\s*%',
        r'(\d+\.?\d*)\s*%\s*(?:apr|interest|annual)',
        r'interest\s+(?:of|at|rate)\s+(\d+\.?\d*)\s*%',
    ]
    
    for pattern in interest_patterns:
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            facts.interest_or_apr_present = True
            try:
                rate = float(match.group(1))
                if facts.interest_rate is None or rate > facts.interest_rate:
                    facts.interest_rate = rate
            except (ValueError, IndexError):
                pass
            # Add quote
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            quotes.append(Quote(field="interest_rate", quote=text[start:end].strip()))
    
    # Late fee detection
    late_fee_patterns = [
        r'\b(?:late fee|late payment fee|penalty|default fee|missed payment fee|overdue charge)',
    ]
    
    for pattern in late_fee_patterns:
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            facts.late_fee_present = True
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            quote_text = text[start:end].strip()
            quotes.append(Quote(field="late_fee", quote=quote_text))
            # Try to extract description
            if not facts.late_fee_description:
                facts.late_fee_description = quote_text[:200]
            break
    
    # Guaranteed return detection
    guarantee_patterns = [
        r'\b(?:guaranteed return|guaranteed profit|capital protected|principal protected|guaranteed|assured return)',
    ]
    
    for pattern in guarantee_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            facts.guaranteed_return_present = True
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                quotes.append(Quote(field="guaranteed_return", quote=text[start:end].strip()))
            break
    
    # Profit sharing detection
    profit_share_patterns = [
        r'\b(?:profit share|profit sharing|revenue share|revenue sharing|musharaka|mudaraba)',
    ]
    
    for pattern in profit_share_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            facts.profit_sharing_present = True
            break
    
    # Repayment structure detection
    if re.search(r'\b(?:installment|monthly payment|fixed payment|emi|equal monthly)', text_lower):
        facts.repayment_structure = "fixed_installments"
    elif re.search(r'\b(?:revenue share|revenue sharing|% of revenue|% of sales)', text_lower):
        facts.repayment_structure = "revenue_share"
    elif re.search(r'\b(?:markup|cost plus|murabaha|cost-plus)', text_lower):
        facts.repayment_structure = "cost_plus_sale"
    
    # Contract type detection
    if facts.interest_or_apr_present and not facts.profit_sharing_present:
        facts.contract_type_guess = "loan"
    elif re.search(r'\b(?:murabaha|cost plus|markup sale)', text_lower):
        facts.contract_type_guess = "murabaha"
    elif re.search(r'\b(?:mudaraba)', text_lower):
        facts.contract_type_guess = "mudaraba"
    elif re.search(r'\b(?:musharaka|partnership)', text_lower):
        facts.contract_type_guess = "musharaka"
    elif re.search(r'\b(?:ijara|lease|rental)', text_lower):
        facts.contract_type_guess = "ijara"
    elif re.search(r'\b(?:wakala|agency)', text_lower):
        facts.contract_type_guess = "wakala"
    
    # Asset backing detection
    asset_patterns = [
        r'\b(?:asset|property|inventory|equipment|commodity|gold|real estate|underlying asset)',
    ]
    
    if any(re.search(p, text_lower, re.IGNORECASE) for p in asset_patterns):
        facts.asset_backing_present = True
    
    # Ambiguity detection
    ambiguity_patterns = [
        r'\b(?:tbd|to be determined|may change|subject to|at our discretion|variable|unclear)',
    ]
    
    for pattern in ambiguity_patterns:
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            facts.ambiguity_flags.append(text[match.start():match.end()])
    
    # Missing info questions
    if facts.contract_type_guess == "unknown":
        facts.missing_info_questions.append("What type of contract is this? (loan, sale, partnership, lease, etc.)")
    if facts.repayment_structure == "unknown":
        facts.missing_info_questions.append("How is repayment structured? (fixed installments, revenue share, cost-plus sale, etc.)")
    if facts.interest_or_apr_present and facts.interest_rate is None:
        facts.missing_info_questions.append("What is the exact interest rate or APR?")
    if facts.late_fee_present and not facts.late_fee_description:
        facts.missing_info_questions.append("How are late fees handled? Are they donated to charity?")
    if facts.guaranteed_return_present:
        facts.missing_info_questions.append("How is the guaranteed return structured? Does it violate risk-sharing principles?")
    
    facts.quotes = quotes
    return facts
