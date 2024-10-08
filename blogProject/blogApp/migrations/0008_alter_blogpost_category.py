# Generated by Django 5.0.7 on 2024-10-07 09:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogApp", "0007_alter_blogpost_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blog_posts",
                to="blogApp.category",
            ),
        ),
    ]