from django.db import models

# Create your models here.


class Input_audios(models.Model):
    keyword = models.TextField(max_length=20)
    audio_1 = models.FileField(upload_to='media')
    audio_2 = models.FileField(upload_to='media')
    audio_3 = models.FileField(upload_to='media')
    audio_analyse = models.FileField(upload_to='media')
    visual_1 = models.FileField(upload_to='media')
    visual_2 = models.FileField(upload_to='media')
    visual_3 = models.FileField(upload_to='media')
    visual_4 = models.FileField(upload_to='media')
    malspec = models.FloatField()
    chroma = models.FloatField()
    zerocross = models.FloatField()
    silence_decible_floor = models.FloatField()
    window_size = models.IntegerField()


class Output_audios(models.Model):
    keyword = models.TextField(max_length= 20)
    search_1 = models.FileField(upload_to='media')
    search_2 = models.FileField(upload_to='media')
    search_3 = models.FileField(upload_to='media')
    search_4 = models.FileField(upload_to='media')
    search_5 = models.FileField(upload_to='media')
    search_6 = models.FileField(upload_to='media')
    visual_1 = models.FileField(upload_to='media')
    visual_2 = models.FileField(upload_to='media')
    visual_3 = models.FileField(upload_to='media')
    visual_4 = models.FileField(upload_to='media')
    visual_5 = models.FileField(upload_to='media')
    visual_6 = models.FileField(upload_to='media')
    runtime = models.IntegerField()
    rmse = models.TextField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    test_audio = models.TextField()
    

class Response(models.Model):
    keyword = models.TextField(max_length= 20)
    file = models.FileField(upload_to='media')
    aud1_response = models.TextField(max_length=20)
    aud2_response = models.TextField(max_length=20)
    aud3_response = models.TextField(max_length=20)
    aud4_response = models.TextField(max_length=20)
    aud5_response = models.TextField(max_length=20)
    aud6_response = models.TextField(max_length=20)

class Plotter(models.Model):
    keyword = models.TextField(max_length=20)
    window_size = models.IntegerField()
    runtime = models.IntegerField()

class Searchkeys(models.Model):
    searchkey = models.TextField(max_length=20)



