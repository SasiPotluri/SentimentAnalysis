# Generated by Django 4.2 on 2023-04-24 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_tweet_alter_tweepytweet_score"),
    ]

    operations = [
        migrations.AddField(
            model_name="tweet",
            name="hashtag",
            field=models.TextField(default=""),
        ),
    ]