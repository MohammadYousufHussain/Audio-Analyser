# Generated by Django 3.0.2 on 2020-05-31 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analyserapp', '0014_searchkeys'),
    ]

    operations = [
        migrations.AddField(
            model_name='output_audios',
            name='rmse',
            field=models.TextField(default='abc'),
            preserve_default=False,
        ),
    ]
