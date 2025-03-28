from typing import List

from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.ocr.ocrspace import OCRSpace
from src.ocr.openai import OCROpenAI
from src.utils.formatting import to_list
from src.utils.logging import logger


def image_to_text(uploaded_file: UploadedFile) -> str:
    ocrs = [OCROpenAI, OCRSpace]

    for ocr in ocrs:
        try:
            result = ocr.parse(file=uploaded_file)
            if result and len(result):
                return result
        except Exception as e:
            logger().info(f"OCR failed for {ocr.__name__}: {str(e)}")

    return ""


def get_list_from_image(file: UploadedFile) -> List[int]:
    return to_list(image_to_text(file))
