import base64


def image_to_base64(file: bytes) -> str:
    """Converts a file uploaded through streamlit into a base64 string"""
    return base64.b64encode(file).decode("utf-8")
