import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Video:
    """Родительский класс"""

    def __init__(self, video_id: str):
        """Инициализирует экземпляр класса Video."""
        self.__video_id = video_id
        self.verify_video_id(video_id)
        try:
            self.video_response = Video.get_service().videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=self.__video_id
            ).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']

        except:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра."""
        return self.title

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=api_key)

    def verify_video_id(self, video_id):
        """Возвращает количество видео, по идентификатору."""
        video_response = self.get_service().videos().list(part='status', id=video_id).execute()
        search_count = video_response['pageInfo']['totalResults']
        return search_count

    @property
    def video_id(self) -> str:
        """Возвращает идентификатор видео."""
        return self.__video_id


class PLVideo(Video):
    """ Дочерний класс для видео в плейлисте."""

    def __init__(self, video_id: str, playlist_id: str):
        """Инициализирует экземпляр класса PLVideo."""
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        """Возвращает идентификатор плейлиста."""
        return self.__playlist_id

    @playlist_id.setter
    def playlist_id(self, value):
        """Устанавливает идентификатор плейлиста."""
        self.__playlist_id = value
