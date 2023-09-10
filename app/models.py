from django.db import models
from django import forms


class HashtagForm(forms.Form):
    hashtag = forms.CharField(max_length=100)


class Tweet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    sentiment = models.CharField(max_length=20)
    hashtag = models.TextField(default='')


class TweepyTweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    tweet_text = models.TextField()
    created_at = models.DateTimeField()
    sentiment = models.OneToOneField('SentimentAnalysis', on_delete=models.CASCADE, null=True)
    score = models.FloatField(default=-12)


class SentimentAnalysis(models.Model):
    tweet = models.ForeignKey(TweepyTweet, null=True, on_delete=models.CASCADE)
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=255)
