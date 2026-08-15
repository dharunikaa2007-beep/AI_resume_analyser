"""
src/text_cleaner.py
Cleans and normalizes unstructured resume text while preserving technical symbols.
"""

import re

# Custom placeholders for sensitive tech tokens
TOKEN_MAP = {
    r"\bc\+\+\b": "TOKEN_CPP",
    r"\bc#\b": "TOKEN_CSHARP",
    r"\.net\b": "TOKEN_DOTNET",
    r"\bnode\.js\b": "TOKEN_NODEJS",
    r"\bci/cd\b": "TOKEN_CICD",
    r"\bscikit-learn\b": "TOKEN_SKLEARN",
}

REVERSE_TOKEN_MAP = {
    "token_cpp": "c++",
    "token_csharp": "c#",
    "token_dotnet": ".net",
    "token_nodejs": "node.js",
    "token_cicd": "ci/cd",
    "token_sklearn": "scikit-learn",
}


def clean_text(text: str) -> str:
    """
    Normalizes text by:
    1. Converting to lowercase
    2. Protecting special technical tokens
    3. Removing URLs, emails, and phone numbers
    4. Removing non-alphanumeric noise
    5. Restoring technical tokens
    6. Collapsing extra whitespace
    """
    if not text or not isinstance(text, str):
        return ""

    normalized = text.lower()

    # Step 1: Protect special tokens
    for pattern, placeholder in TOKEN_MAP.items():
        normalized = re.sub(pattern, placeholder, normalized, flags=re.IGNORECASE)

    # Step 2: Remove URLs and contact details (irrelevant for skill matching)
    normalized = re.sub(r"http\S+|www\.\S+", " ", normalized)
    normalized = re.sub(r"\S+@\S+", " ", normalized)
    normalized = re.sub(r"\+?\d[\d -]{8,12}\d", " ", normalized)

    # Step 3: Remove unwanted special characters, keeping alphanumeric and underscores
    normalized = re.sub(r"[^\w\s]", " ", normalized)

    # Step 4: Restore protected tokens
    for token_placeholder, original_skill in REVERSE_TOKEN_MAP.items():
        normalized = re.sub(rf"\b{token_placeholder}\b", original_skill, normalized, flags=re.IGNORECASE)

    # Step 5: Normalize extra spaces and newlines
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized