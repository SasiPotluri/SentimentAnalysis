from django.urls import path
from .views import authenticate, retrieve_tweets, my_analysis, my_search
urlpatterns = [
    path('authenticate/', authenticate, name='authenticate_twitter'),
    path('authenticate/retrieve_tweets/', retrieve_tweets, name='tweets'),
    path('authenticate/my_analysis/', my_analysis, name='Analysis'),
    path('authenticate/search/', my_search, name='Search'),
]
