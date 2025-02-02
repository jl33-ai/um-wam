import requests

from utils.config import get_secret
from utils.formatting import to_list

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


def extract_list_from_image(my_upload):
    result = do_request(my_upload)
    ocr_text = result.get('ParsedResults')[0].get('ParsedText')

    grade_list = to_list(ocr_text)
    return grade_list
