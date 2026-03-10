import re

def preprocess_email(email_text: str) -> str:
    """
    Clean email: lowercase, remove extra whitespace, strip signatures/headers if present.
    """
    # Basic cleaning
    email_text = email_text.lower().strip()
    # Remove common signature patterns (e.g., --, Best regards)
    email_text = re.sub(r'--\s*\n.*', '', email_text, flags=re.DOTALL | re.IGNORECASE)
    email_text = re.sub(r'best regards.*', '', email_text, flags=re.DOTALL | re.IGNORECASE)
    # Normalize whitespace
    email_text = re.sub(r'\s+', ' ', email_text)
    return email_text