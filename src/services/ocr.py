import requests

from src.config import get_secret
from src.utils.formatting import to_list

API_URL = 'https://api.ocr.space/parse/image'

API_KEY = get_secret("OCR_API_KEY")

LANGUAGE = 'eng'


def do_request(file_stream):
    payload = {
        'apikey': API_KEY,
        'language': LANGUAGE,
    }
    response = requests.post(
        API_URL,
        files={file_stream.name: file_stream},
        data=payload,
    )

    return response.json()


def extract_list_from_image(file):
    try:
        result = do_request(file)
    except Exception as e:
        return []

    if not result:
        return []

    try:
        parsed_results = result.get('ParsedResults')
        if not parsed_results or not isinstance(parsed_results, list):
            return []

        first_result = parsed_results[0]
        if not isinstance(first_result, dict):
            return []

        ocr_text = first_result.get('ParsedText')
        if not ocr_text or not isinstance(ocr_text, str):
            return []

        return to_list(ocr_text)

    except (AttributeError, IndexError, KeyError) as e:
        return []
