import fitz






def create_report(extracted_text: str, ruling_llm_response):
    """
    Creates a compliance report based on extracted text and LLM response.
    """
    doc = fitz.open()
    pass