# Generated by Django 4.2.6 on 2023-11-08 23:11

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_remove_post_tag_alter_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=post.models.user_directory_path, verbose_name='Picture'),
        ),
    ]
