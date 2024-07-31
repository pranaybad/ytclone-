from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addvideo/', views.addvideo, name='addvideo'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('youtube_upload/', views.youtube_upload, name='youtube_upload'),
]
