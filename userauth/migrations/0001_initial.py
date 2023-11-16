# Generated by Django 4.2.6 on 2023-11-08 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0005_remove_post_tag_alter_post_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('bio', models.TextField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to=userauth.models.user_directory_path, verbose_name='Picture')),
                ('favourite', models.ManyToManyField(to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
