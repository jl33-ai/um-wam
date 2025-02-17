import requests
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.config import get_secret
from src.ocr.abstract import OCRService

API_URL = 'https://api.ocr.space/parse/image'

API_KEY = get_secret("OCR_API_KEY")

LANGUAGE = 'eng'


class OCRSpace(OCRService):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _request(file: UploadedFile):
        payload = {
            'apikey': API_KEY,
            'language': LANGUAGE,
        }
        response = requests.post(
            API_URL,
            files={file.name: file},
            data=payload,
        )

        return response.json()

    @staticmethod
    def parse(file: UploadedFile):
        try:
            result = OCRSpace._request(file)
        except Exception as e:
            return ""

        if not result:
            return ""

        try:
            parsed_results = result.get('ParsedResults')
            if not parsed_results or not isinstance(parsed_results, list):
                return ""

            first_result = parsed_results[0]
            if not isinstance(first_result, dict):
                return ""

            text = first_result.get('ParsedText')
            if not text or not isinstance(text, str):
                return ""

            return text

        except (AttributeError, IndexError, KeyError) as e:
            return ""
