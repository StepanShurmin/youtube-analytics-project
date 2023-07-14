import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

api_key: str = os.getenv('YT_API_KEY')


class PlayList:
    """Класс плейлист."""

    def __init__(self, playlist_id):
        """Инициализация экземпляра класса."""
        self.playlist_id = playlist_id
        self.title = self.get_service().playlists().list(
            id=playlist_id, part='snippet').execute()['items'][0]['snippet']['title']

        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.__video_data = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                    part='contentDetails, snippet',
                                                                    maxResults=50,
                                                                    ).execute()

        self.__video_id = [video['contentDetails']['videoId'] for video in self.__video_data['items']]

        self.__video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                                 id=','.join(self.__video_id)
                                                                 ).execute()

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def total_duration(self) -> timedelta:
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста."""
        total_duration = timedelta()

        for video in self.__video_response['items']:
            encoded_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(encoded_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста."""

        max_likes_video = max(self.__video_response['items'], key=lambda video: int(video['statistics']['likeCount']))
        result_url = f"https://youtu.be/{max_likes_video['id']}"

        return result_url
