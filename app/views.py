import io
import random

import tweepy
from django.shortcuts import render
from tweepy import OAuthHandler, API
from textblob import TextBlob
from .models import TweepyTweet, SentimentAnalysis, HashtagForm, Tweet
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
import base64

# Create an instance of the Twitter API
api = API()


def authenticate(request):
    if request.method == 'POST':
        consumer_key = request.POST['consumer_key']
        consumer_secret = request.POST['consumer_secret']
        access_token = request.POST['access_token']
        access_token_secret = request.POST['access_token_secret']
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api.auth = auth
        tweets = api.user_timeline(screen_name=request.user.username, count=200, tweet_mode="extended")
        print(tweets)
        # Extract relevant information from the tweets and store in the database
        for tweet in tweets:
            tweet_text = tweet.full_text
            tweet_id = tweet.id
            tweet_created_at = tweet.created_at
            tweet_sentiment = analyze_sentiment(tweet_text)
            sentiment_analysis = SentimentAnalysis(sentiment_score=tweet_sentiment)
            sentiment_analysis.save()
            tweet = TweepyTweet(tweet_id=tweet_id, tweet_text=tweet_text, created_at=tweet_created_at,
                                score=tweet_sentiment)
            tweet.save()
        tweets = TweepyTweet.objects.filter(tweet_id__isnull=False).order_by('created_at')
        sorted_tweets = sorted(tweets, key=lambda x: x.created_at, reverse=True)
        context = {
            'tweets': sorted_tweets
        }

        return render(request, 'retrieve_tweets.html', context)

    else:
        return render(request, 'authenticate.html')


def retrieve_tweets(request):
    tweets = TweepyTweet.objects.filter(tweet_id__isnull=False).order_by('created_at')
    sorted_tweets = sorted(tweets, key=lambda x: x.created_at, reverse=True)
    context = {
        'tweets': sorted_tweets
    }

    return render(request, 'retrieve_tweets.html', context)


def analyze_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    sentiment_score = analysis.sentiment.polarity
    return sentiment_score


def my_analysis(request):
    tweets = TweepyTweet.objects.filter(tweet_id__isnull=False).order_by('created_at')
    positive_tweets = TweepyTweet.objects.filter(score__gt=0.00).count()
    neutral_tweets = TweepyTweet.objects.filter(score=0.00).count()
    negative_tweets = TweepyTweet.objects.filter(score__lt=0.00).count()

    # Generate pie chart
    labels = ['Positive', 'Neutral', 'Negative']
    values = [positive_tweets, neutral_tweets, negative_tweets]
    colors = ['#00FF00', '#FFFF00', '#FF0000']
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Sentiment Analysis')
    pie_chart_buffer = BytesIO()
    plt.savefig(pie_chart_buffer, format='png')
    pie_chart_buffer.seek(0)
    pie_chart_image = base64.b64encode(pie_chart_buffer.getvalue()).decode('utf-8')
    plt.close()

    # Generate wordcloud
    wordcloud_text = " ".join([tweet.tweet_text for tweet in tweets])

    # Create a word cloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white')
    wordcloud.generate(wordcloud_text)

    # Convert the word cloud image to a base64 string
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    wordcloud_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'my_analysis.html', {'pie_chart_image': pie_chart_image, 'wordcloud_image': wordcloud_image})


def my_search(request):
    if request.method == 'POST':
        form = HashtagForm(request.POST)
        if form.is_valid():
            hashtag = form.cleaned_data['hashtag']
            tweets = tweepy.Cursor(api.search_tweets, q=hashtag, lang='en', tweet_mode='extended').items(100)

            # Save tweets and perform sentiment analysis
            for tweet in tweets:
                tweet_text = tweet.full_text
                tweet_date = tweet.created_at
                sentiment = analyze_sentiment(tweet_text)
                Tweet.objects.create(hashtag=hashtag, text=tweet_text, created_at=tweet_date, sentiment=sentiment)

            # Retrieve all tweets with sentiment analysis results
            tweet_list = Tweet.objects.filter(hashtag=hashtag)

            # Render the analysis in an HTML template
            return render(request, 'analysis.html', {'tweets': tweet_list})
    else:
        form = HashtagForm()

    return render(request, 'search.html', {'form': form})