from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
from googleapiclient.discovery import build


# Create your views here.
def home(request):
    youtube = build('youtube', 'v3',
                    developerKey=settings.YOUTUBE_API_DATA_KEY)

    def get_channel_videos(channel_id):
        res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos = []
        next_page_token = None
        while 1:
            res1 = youtube.playlistItems().list(playlistId=playlist_id,
                                                part='snippet',
                                                maxResults=20,
                                                pageToken=next_page_token).execute()
            videos += res1['items']
            next_page_token = res1.get('nextPageToken')
            if next_page_token is None:
                break
        return videos

    videos = get_channel_videos('UCiBJGpHQKvwZ5xUg0LU_EfQ')
    print(len(videos))
    context = {
        'videos': videos
    }
    return render(request, 'videos/home.html', context)


def videos_details(request, videoId):
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet',
        'id': videoId,
        'key': settings.YOUTUBE_API_DATA_KEY
    }
    r = requests.get(video_url, params=params)
    video = r.json()['items'][0]

    context = {
        'video' : video
    }

    return render(request, 'videos/video_details.html',context)

def create_playlist(request):
    url = 'https://developers.google.com/youtube/v3/docs/playlists/insert'
    return HttpResponse('OK')
