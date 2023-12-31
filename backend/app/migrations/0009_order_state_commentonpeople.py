# Generated by Django 4.2.6 on 2023-12-19 08:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_user_motto'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='CommentOnPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('txt', models.TextField()),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='app.user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='app.user')),
            ],
        ),
    ]
