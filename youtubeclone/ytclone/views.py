from django.shortcuts import render, redirect
from .models import Video
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm


from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from django.shortcuts import redirect, render
import os
from googleapiclient.http import MediaIoBaseUpload
import io
from googleapiclient.errors import HttpError

import tempfile
# admin pranay is user name and password

# def fetch_youtube_data(query='', max_results=5):
#     api_key = settings.YOUTUBE_API_KEY
#     base_url = 'https://www.googleapis.com/youtube/v3/search'
#     # below the data is fake or dummy data we dont need this in presentation. jus remove all the array and dummy_data = [] and only put videos=[] thats it ---> also when add new api in seeting file that time enable youtube v3 in google console api 
# #     videos = [
# #     {
# #         'title': 'Introduction to Python Programming',
# #         'thumbnail_url': 'https://i.ytimg.com/vi/UrsmFxEIp5k/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCgVi5ujXAKguur03EW6bRz2JX6Hg',
# #         'video_url': 'https://www.youtube.com/watch?v=UrsmFxEIp5k&t=27575s',
# #         'views': '1.2M',
# #         'upload_date': '2024-07-25T10:00:00Z'
# #     },
# #     {
# #         'title': 'Learn Django in 30 Minutes',
# #         'thumbnail_url': 'https://i.ytimg.com/vi/5qZ5sh9tbb8/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBkGTL4I6WVKbmLKcrobXekp-VW2g',
# #         'video_url': 'https://www.youtube.com/watch?v=5qZ5sh9tbb8',
# #         'views': '300K',
# #         'upload_date': '2024-07-26T14:00:00Z'
# #     },
# #     {
# #         'title': 'Understanding SQL Queries',
# #         'thumbnail_url': 'https://i.ytimg.com/vi/yFlarM35vxA/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBX5rLm5CCK4jbnn319sv8qBPp3og',
# #         'video_url': 'https://www.youtube.com/watch?v=yFlarM35vxA',
# #         'views': '450K',
# #         'upload_date': '2024-07-27T08:00:00Z'
# #     },
# #     {
# #         'title': 'Advanced JavaScript Techniques',
# #         'thumbnail_url': 'https://i.ytimg.com/vi/RaVhSLVg9Bw/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLA-NCwkKEY4VIhn0Rj4dKDltDPycA',
# #         'video_url': 'https://www.youtube.com/watch?v=RaVhSLVg9Bw',
# #         'views': '850K',
# #         'upload_date': '2024-07-28T16:00:00Z'
# #     },
# #     {
# #         'title': 'Building Responsive Websites with Tailwind CSS',
# #         'thumbnail_url': 'https://i.ytimg.com/vi/ytYy9EVpI_Q/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLBDsJenNO_VW6UkKxgokXKaDkccQQ',
# #         'video_url': 'https://www.youtube.com/watch?v=ytYy9EVpI_Q',
# #         'views': '600K',
# #         'upload_date': '2024-07-29T12:00:00Z'
# #     }
# # ]

#     # dummy_data = [] 
#     videos=[] 
#     # <- change this with dummy datat when i use real api in final presentation
#     next_page_token = None

#     while True:
#         url = f"{base_url}?part=snippet&q={query}&type=video&key={api_key}&maxResults={max_results}"
#         if next_page_token:
#             url += f"&pageToken={next_page_token}"
        
#         response = requests.get(url)
#         data = response.json()
        
#         print("API Response:", data)  
        

#         if response.status_code != 200:
#             print("Error fetching data from YouTube API:", response.status_code, data)
#             break
        
      
#         for item in data.get('items', []):
#             video = {
#                 'title': item['snippet']['title'],
#                 'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
#                 'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
#                 'views': 'N/A',  
#                 'upload_date': item['snippet']['publishedAt'],
#             }
#             videos.append(video)
        
#         next_page_token = data.get('nextPageToken')
#         if not next_page_token:
#             break

#     return videos


def fetch_youtube_data(query='', max_results=5, max_pages=2):
    api_key = settings.YOUTUBE_API_KEY
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    videos = []
    next_page_token = None
    pages_fetched = 0

    while pages_fetched < max_pages:
        url = f"{base_url}?part=snippet&q={query}&type=video&key={api_key}&maxResults={max_results}"
        if next_page_token:
            url += f"&pageToken={next_page_token}"

        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            print("Error fetching data from YouTube API:", response.status_code, data)
            break
        
        for item in data.get('items', []):
            video = {
                'title': item['snippet']['title'],
                'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'views': 'N/A',  
                'upload_date': item['snippet']['publishedAt'],
            }
            videos.append(video)

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

        pages_fetched += 1

    return videos


def search(request):
    query = request.GET.get('q', '')
    if query:
        video_data = fetch_youtube_data(query)
    else:
        video_data = []
    
    return render(request, 'searchresults.html', {'data': video_data, 'query': query})

def index(request):
    query = request.GET.get('q', '')  
    video_data = fetch_youtube_data(query)
    context = {'data': video_data, 'query': query,'user': request.user}
    return render(request, 'index.html', context)

def addvideo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_url = request.POST.get('video_url')
        thumbnail_url = request.POST.get('thumbnail_url')
        
        video = Video(
            title=title,
            description=description,
            video_url=video_url,
            thumbnail_url=thumbnail_url
        )
        video.save()
        
    return render(request, 'addvideo.html')


# add profile

def profile(request):
    return render(request, 'userprofile.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user.username)
            login(request, user)
            return redirect('index')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserRegistrationForm()
    
    return render(request, 'signup.html', {'form': form})


# CLIENT_SECRETS_FILE = "ytclone/client_secrets.json"
# SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def youtube_upload(request):
    if request.method == 'POST':
        video_title = request.POST.get('title')
        video_description = request.POST.get('description')
        video_file = request.FILES['video']

        # OAuth flow
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR, 'ytclone/client_secrets.json')

        if not os.path.exists(CLIENT_SECRETS_FILE):
            return render(request, 'upload_video.html', {'error': 'Client secrets file not found.'})

        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        youtube = build('youtube', 'v3', credentials=credentials)

        # Create file-like object from uploaded file
        video_file_io = io.BytesIO(video_file.read())
        media_body = MediaIoBaseUpload(video_file_io, mimetype='video/mp4', chunksize=-1, resumable=True)

        request_body = {
            'snippet': {
                'title': video_title,
                'description': video_description,
                'tags': ['django', 'api', 'youtube'],
                'categoryId': '22',
            },
            'status': {
                'privacyStatus': 'public',
                'embeddable': True,
                'license': 'youtube',
            }
        }

        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_body
        )

        try:
            response = request.execute()
            return render(request, 'upload_success.html', {'video_id': response['id']})
        except HttpError as error:
            return render(request, 'upload_video.html', {'error': f'An error occurred: {error}'})
    else:
        return render(request, 'upload_video.html')
