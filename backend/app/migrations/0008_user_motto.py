# Generated by Django 4.2.6 on 2023-12-19 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_firstcomment_secondcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='motto',
            field=models.TextField(default='这个人还没有设置个人简介'),
        ),
    ]