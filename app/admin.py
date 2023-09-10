from django.contrib import admin
from . models import TweepyTweet, SentimentAnalysis
# Register your models here.
admin.site.register(TweepyTweet)
admin.site.register(SentimentAnalysis)
