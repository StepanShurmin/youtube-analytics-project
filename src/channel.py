import os
import json

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется. Дальше получает необходимые атрибуты."""
        self._channel_id = channel_id
        self.channel = Channel.get_service().channels().list(
            id=channel_id, part='snippet,statistics'
        ).execute()

        self.id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/{self.channel['items'][0]['snippet']['customUrl']}"
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        """Возвращает значение поля channel_id."""
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        """Устанавливает значение поля channel_id и генерирует исключение AttributeError."""
        return AttributeError

    def to_json(self, path):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(path, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dump(self.channel, indent=2, ensure_ascii=False))
