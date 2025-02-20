from abc import ABC, abstractmethod

from streamlit.runtime.uploaded_file_manager import UploadedFile


class OCRService(ABC):
    @staticmethod
    @abstractmethod
    def _request(file: UploadedFile) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def parse(file: UploadedFile) -> str:
        pass
