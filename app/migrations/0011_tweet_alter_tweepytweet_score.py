# Generated by Django 4.2 on 2023-04-24 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_tweepytweet_score"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tweet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField()),
                ("sentiment", models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name="tweepytweet",
            name="score",
            field=models.FloatField(default=-12),
        ),
    ]
