# Generated by Django 3.0.2 on 2020-05-24 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analyserapp', '0010_auto_20200517_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='input_audios',
            name='window_size',
            field=models.IntegerField(default=3000),
            preserve_default=False,
        ),
    ]
