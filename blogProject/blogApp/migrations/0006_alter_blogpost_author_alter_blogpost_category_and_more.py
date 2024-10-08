# Generated by Django 5.0.7 on 2024-10-07 09:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogApp", "0005_remove_blogpost_created_at_remove_blogpost_tags_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="category",
            field=models.CharField(default="Default Category", max_length=255),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
