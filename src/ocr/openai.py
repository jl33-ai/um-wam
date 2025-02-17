import requests
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.config import get_secret
from src.ocr.abstract import OCRService
from src.utils.encoding import *

API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = get_secret("OPENAI_API_KEY")


class OCROpenAI(OCRService):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _request(file: UploadedFile):
        base64_data = image_to_base64(file.getvalue())
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "return the numbers in this image, in order, delimited by spaces. the only thing in your response should be the numbers.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_data}"},
                        },
                    ],
                }
            ],
        }
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
        )

        return response.json()

    @staticmethod
    def parse(file: UploadedFile):
        try:
            result = OCROpenAI._request(file)
        except Exception as e:
            return ""

        if not result:
            return ""

        try:
            values = result["choices"][0]["message"]["content"]
            if not values or not isinstance(values, str):
                return ""

        except (AttributeError, IndexError, KeyError) as e:
            return ""

        return values
