"""
Helper functions for Streamlit pages.
"""

def safe_get(dictionary, key, default='N/A'):
    """Safely get value from dictionary with default."""
    value = dictionary.get(key)
    return value if value is not None else default