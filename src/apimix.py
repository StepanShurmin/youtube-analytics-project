import os

from googleapiclient.discovery import build


class ApiMixin:
    api_key: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=cls.api_key)
