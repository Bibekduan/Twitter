# Generated by Django 4.2.6 on 2023-11-08 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
