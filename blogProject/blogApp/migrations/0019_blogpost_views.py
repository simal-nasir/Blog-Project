# Generated by Django 5.0.7 on 2024-10-15 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogApp", "0018_comment_is_flagged"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
