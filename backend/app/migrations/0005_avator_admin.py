# Generated by Django 4.2.6 on 2023-12-02 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_avator_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='avator',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.administrator'),
        ),
    ]
