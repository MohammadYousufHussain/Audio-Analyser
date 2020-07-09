from __future__ import print_function
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import Input_audios, Output_audios, Response, Plotter, Searchkeys
import pandas as pd
import numpy as np
import time, datetime
import librosa
import librosa.display
from sklearn.metrics import mean_squared_error
from sklearn.metrics import max_error
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.playback import play
import wave
import os
from django.http import HttpResponse
import librosa.display as ld
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import itertools, ast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions



# Create your views here.

def jsaudio(request):
    return render(request,'jsresults.html')

def chart(request):
    return render(request,'chart.html')

class Chartdata(APIView):
   
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataobj = Plotter.objects.all()
        objs = []
        for i in dataobj:
            objs.append(i)
        window = []
        runtime = []
        objs.sort(key=lambda x: x.window_size)
        for i in objs:
            window.append(i.window_size)
            runtime.append(i.runtime)

        
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        data = {
        "window_size": window,
        "runtime": runtime
    }
        #usernames = [user.username for user in User.objects.all()]
        return Response(data)


#Function to fetch the homepage
def home(request):
    return render(request,'home.html')

#Function to fetch the audio samples based on keyword (Search bar)
def search(request):
    print("search invoked")
    searchobj = Searchkeys()
    found = False
    word = request.GET['searchbar']
    objs = Input_audios.objects.all()
    for i in objs:
        if i.keyword == word:
            inobj = i
            found = True
    objout = Output_audios.objects.all()
    for j in objout:
        if j.keyword == word:
            outobj = j
    if found == True:
        searchobj.searchkey = word
        searchobj.save()
        return render(request,'jsaudioresults.html',{'audio': outobj,'inaudio':inobj})
    else:
        return render(request,'home.html',{'input': "Keyword not found"})




#Function to upload the audio samples and to process them
def file_upload(request):
    input_file = Input_audios()
    def_audio = Input_audios.objects.all()
    word = request.POST['keyword']
    word = word.lower()
    
    file1 = request.FILES['audio1']
    try:
        file2 = request.FILES['audio2']
    except:
        file2 = request.FILES['audio1']
        pass
    
    try:
        file3 = request.FILES['audio3']
    except:
        file3 = request.FILES['audio1']
        
    
    malspec = float(request.POST['malspec'])
    chroma = float(request.POST['chroma'])
    zerocross = float(request.POST['zerocross'])
    sdf = float(request.POST['sdf'])
    print(request.POST['default_audio'])
    window_size = int(request.POST['window_size'])
    

    if str(request.POST['default_audio']) == "Need_default_audio":
        for i in def_audio:
            obj = i
            input_file.audio_analyse = obj.audio_analyse
            break
    else:

        file_analyse = request.FILES['analyse']
        input_file.audio_analyse = file_analyse
       
    

    input_file.keyword = word
    input_file.audio_1 = file1
    input_file.audio_2 = file2
    input_file.audio_3 = file3
    input_file.chroma = chroma
    input_file.malspec = malspec
    input_file.zerocross = zerocross
    input_file.silence_decible_floor = sdf
    input_file.window_size = window_size

    input_file.save()

    plotobj = Plotter()
    plotobj.keyword = word
    plotobj.window_size = window_size
    plotobj.runtime = 0
    plotobj.save()

    obj = Input_audios.objects.last()
    
    audio1 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + str(obj.audio_1)[5:]
    audio2 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + str(obj.audio_2)[5:]
    audio3 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + str(obj.audio_3)[5:]
    audioanalyse = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + str(obj.audio_analyse)[5:]
    print('clicked')
    search_function(malspec, chroma, zerocross, sdf, keyword = word, keyword_file1= audio1, keyword_file2=audio2, keyword_file3 = audio3,
                    large_audio_file=audioanalyse)

    
    
    "=========="
    
    
    loc = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\"
    filestr1 = obj.audio_1
    filestr1 = str(filestr1)
    filestr2 = obj.audio_2
    filestr2 = str(filestr2)
    filestr3 = obj.audio_3
    filestr3 = str(filestr3)
    filestr4 = obj.audio_analyse
    filestr4 = str(filestr4)
    
    aud1_file = loc + filestr1[6:]
    print(loc + filestr1)
    obj.visual_1 = visualisation(aud1_file,1)
    
    aud2_file = loc + filestr2[6:]
    obj.visual_2 = visualisation(aud2_file,1)
    aud3_file = loc + filestr3[6:]
    obj.visual_3 = visualisation(aud3_file,1)
    aud4_file = loc + filestr4[6:]
    obj.visual_4 = visualisation(aud4_file,1)
    
    obj.save()
    
    "==========="
    
    
    
    
    output_files = Output_audios.objects.last()
    return render(request,'jsresults.html',{'audio': output_files,'inaudio':obj})


#funtion to plot graphs based on window size and runtime

def plotter(request):

    plotobj = Plotter.objects.all()
    plotobj1 = []
    for i in plotobj:
        plotobj1.append(i)
    plotobj1.sort(key=lambda x: x.window_size)
    windowlist = []
    runtimelist = []
    data = {'Keyword': [], 'Window_size': [], 'Runtime': []}
    for i in plotobj1:
        data['Keyword'].append(i.keyword)
        data['Window_size'].append(i.window_size)
        data['Runtime'].append(i.runtime)
    
    dataframe = pd.DataFrame(data, columns = ['Window_size','Runtime'])
    dataframe.plot(x = 'Window_size', y = 'Runtime', kind  = 'line')
    plt.savefig('C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\static\\graph1.jpg')

    return render(request,'chart.html',{'plotobj':plotobj})


    '''
    in_obj = Input_audios.objects.all()
    out_obj = Output_audios.objects.all()
    windowlist = []
    runtimelist = []
    sample = []
    data = {'Window_size': [], 'Runtime': []}
    for i in in_obj:
        data['Window_size'].append(i.window_size)
    for i in out_obj:
        data['Runtime'].append(i.runtime)
    windowlist = data['Window_size']
    runtimelist = data['Runtime']
    l = len(windowlist)
    for i in range(0,l):
        sample.append(i)

    
    dataframe = pd.DataFrame(data, columns = ['Window_size','Runtime'])
    dataframe.plot(x = 'Window_size', y = 'Runtime', kind  = 'scatter')
    plt.savefig('C:\\Users\\PSSRE\\Downloads\\graph.jpg')

    return render(request,'datapage.html',{'data': data, 'windowlist': windowlist, 'runtimelist': runtimelist})
    '''
    



#Function to fetch the result with the default audio sample
def result_page(request):
    input_files = Input_audios.objects.all()
    for i in input_files:
        obj = i
        break
    new_row = Input_audios()
    new_row = obj
    new_row.save()

    output_files = Output_audios.objects.all()
    for j in output_files:
        outobj = j
        break
    return render(request,'jsdefresults.html',{'audio': outobj,'inaudio':obj})


#Funciton to submit the review data submitted in audioresult page
def datasubmit(request):
    aud1_output = request.GET['aud_1match']
    aud2_output = request.GET['aud_2match']
    aud3_output = request.GET['aud_3match']
    aud4_output = request.GET['aud_4match']
    aud5_output = request.GET['aud_5match']
    aud6_output = request.GET['aud_6match']
    myresponse = Response()
    myresponse.aud1_response = aud1_output
    myresponse.aud2_response = aud2_output
    myresponse.aud3_response = aud3_output
    myresponse.aud4_response = aud4_output
    myresponse.aud5_response = aud5_output
    myresponse.aud6_response = aud6_output
    
    obj = Input_audios.objects.last()
    myresponse.file = obj.audio_analyse
    myresponse.keyword = obj.keyword

    myresponse.save()

    return render(request,'lastpage.html')

def visualisation(fname,n):
    print(fname)
    #y,sr = librosa.load(librosa.util.example_audio_file(),duration = 10)
    #y,sr = librosa.load('C:\\Users\\PSSRE\\Downloads\\Voice_042.wav',duration = 2)
    y,sr = librosa.load(fname)
    plt.figure(figsize=(12,6))
    #plt.figure()
    #plt.subplot(2,1,1)
    ld.waveplot(y,sr=sr)
    #plt.title('Monophonic')
    file_name = fname + ".jpg"
    plt.savefig(file_name)
    current_time = datetime.datetime.now()
    timestr = str(current_time.year) + "_" + str(current_time.month) + "_" + str(current_time.day) + "_" + str(current_time.hour) + "_" + str(current_time.minute) + "_" + str(current_time.second)
    #output.search_1 = "media/search_1" + timestr
    if n==2:
        f1 = fname.split('media\media\\')
        f2 = f1[1]
        #saved_file = 'media/' + fname[len(fname)-21:] + ".jpg"
        saved_file = 'media/' + f2 + ".jpg"
        #saved_file = "media/" + fname[len(fname)-26:] + ".jpg"
    else:
        f1 = fname.split('media\media\\')
        f2 = f1[1]
        #saved_file = 'media/' + fname[len(fname)-21:] + ".jpg"
        saved_file = 'media/' + f2 + ".jpg"
    return saved_file
    

"********************plot***************************"

class Resultplot1(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        audobj = Input_audios.objects.last()
        outobj = Output_audios.objects.last()
        rmse = outobj.rmse
        print('rmse :',rmse)
        aud1 = str(audobj.audio_1)
        audb = str(audobj.audio_analyse)
        search1 = str(outobj.search_1)
        search2 = str(outobj.search_2)
        search3 = str(outobj.search_3)
        itemlist = []
        audplots = []
        columnplots = []
        itemlist.append(aud1)
        itemlist.append(audb)
        itemlist.append(search1)
        itemlist.append(search2)
        itemlist.append(search3)
        for i in itemlist:
            fname = i.split('media/')
            fname = fname[1]
            fname = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + fname
            audioplot,sr = librosa.load(fname,sr=15000) 
            
            columns = []
            count = 0
            for i in range(0,len(audioplot)):
                columns.append(count)
                count += 1/sr
                count = round(count,8)
            audplots.append(audioplot)
            columnplots.append(columns)
        
        rmse = outobj.rmse
        audlen = len(audplots[1])
        rmse = ast.literal_eval(rmse)
        rmse_len = audlen//len(rmse)
        new_list = new_rmse_list(rmse_list = rmse, repeat_times = rmse_len)
        lentime = []
        start_time = outobj.start_time
        end_time = outobj.end_time
        test_audio = outobj.test_audio
        test_audio = ast.literal_eval(test_audio)
        

        start_point = float(start_time * audlen/len(test_audio))
        

        end_point = float(end_time * audlen/len(test_audio))
        
        for i in range(0,audlen):
            
            if i> start_point and i<end_point:
                lentime.append(1)
            else:
                lentime.append(0)

            
        data = {
            'keyaud' : audplots[0],
            'keysr' : columnplots[0],
            'bigaud' : audplots[1],
            'bigsr' : columnplots[1],
            'search1aud' : audplots[2],
            'search1sr' : columnplots[2],
            'search2aud' : audplots[3],
            'search2sr' : columnplots[3],
            'search3aud' : audplots[4],
            'search3sr' : columnplots[4],
            'rmse':new_list,
            'lentime': lentime
                
        
        
        }
        
        return Response(data)


#function to fetch the searched keyword

class Searchplot(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        keyword = Searchkeys.objects.last()
        print('keyword: ',keyword.searchkey)
        inall = Input_audios.objects.all()
        outall = Output_audios.objects.all()
        for i in inall:
            if i.keyword == keyword.searchkey.lower():
                audobj = i
                break
        for i in outall:
            if i.keyword == keyword.searchkey.lower():
                outobj = i
                break
            

        #audobj = Input_audios.objects.last()
        #outobj = Output_audios.objects.last()
        aud1 = str(audobj.audio_1)
        audb = str(audobj.audio_analyse)
        search1 = str(outobj.search_1)
        search2 = str(outobj.search_2)
        search3 = str(outobj.search_3)

        itemlist = []
        audplots = []
        columnplots = []
        itemlist.append(aud1)
        itemlist.append(audb)
        itemlist.append(search1)
        itemlist.append(search2)
        itemlist.append(search3)
        for i in itemlist:
            fname = i.split('media/')
            fname = fname[1]
            fname = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + fname
            audioplot,sr = librosa.load(fname,sr=15000) 
            
            columns = []
            count = 0
            for i in range(0,len(audioplot)):
                columns.append(count)
                count += 1/sr
                count = round(count,8)
            audplots.append(audioplot)
            columnplots.append(columns)
        rmse = outobj.rmse
        audlen = len(audplots[1])
        rmse = ast.literal_eval(rmse)
        rmse_len = audlen//len(rmse)
        new_list = new_rmse_list(rmse_list = rmse, repeat_times = rmse_len)
        lentime = []
        start_time = outobj.start_time
        end_time = outobj.end_time
        test_audio = outobj.test_audio
        test_audio = ast.literal_eval(test_audio)
        

        start_point = float(start_time * audlen/len(test_audio))
        

        end_point = float(end_time * audlen/len(test_audio))
        
        for i in range(0,audlen):
            
            if i> start_point and i<end_point:
                lentime.append(1)
            else:
                lentime.append(0)

            
        data = {
            'keyaud' : audplots[0],
            'keysr' : columnplots[0],
            'bigaud' : audplots[1],
            'bigsr' : columnplots[1],
            'search1aud' : audplots[2],
            'search1sr' : columnplots[2],
            'search2aud' : audplots[3],
            'search2sr' : columnplots[3],
            'search3aud' : audplots[4],
            'search3sr' : columnplots[4],
            'rmse': new_list,
            'lentime': lentime
                
        
        
        }
        
        return Response(data)


#function for default results

class Defresults(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        inall = Input_audios.objects.all()
        outall = Output_audios.objects.all()
        for i in inall:
            audobj = i
            break
        for i in outall:
            outobj = i
        #audobj = Input_audios.objects.last()
        #outobj = Output_audios.objects.last()
        aud1 = str(audobj.audio_1)
        audb = str(audobj.audio_analyse)
        rmse = outobj.rmse
        start_time = outobj.start_time
        end_time = outobj.end_time
        test_audio = outobj.test_audio
        test_audio = ast.literal_eval(test_audio)

        print('length of test audio: ', len(test_audio))
        #start_time = 5000
        #end_time = 7000
        
        search1 = str(outobj.search_1)
        search2 = str(outobj.search_2)
        search3 = str(outobj.search_3)
        itemlist = []
        audplots = []
        columnplots = []
        itemlist.append(aud1)
        itemlist.append(audb)
        itemlist.append(search1)
        itemlist.append(search2)
        itemlist.append(search3)
        for i in itemlist:
            fname = i.split('media/')
            fname = fname[1]
            fname = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\" + fname
            audioplot,sr = librosa.load(fname, sr = 5000) 
            
            
            columns = []
            
            count = 0
            
            for i in range(0,len(audioplot)):
                columns.append(count)
                count += 1/sr
                count = round(count,8)
            audplots.append(audioplot)
            columnplots.append(columns)
        
        audlen = len(audplots[1])
        rmse = ast.literal_eval(rmse)
        rmse_len = audlen//len(rmse)
        
        lentime = []
        start_time = outobj.start_time
        end_time = outobj.end_time
        test_audio = outobj.test_audio
        test_audio = ast.literal_eval(test_audio)
        

        start_point = float(start_time * audlen/len(test_audio))
        

        end_point = float(end_time * audlen/len(test_audio))
        
        for i in range(0,audlen):
            
            if i> start_point and i<end_point:
                lentime.append(audplots[1][i])
                
                audplots[1][i]=0
                
            else:
                lentime.append(0)
        
            
        

        

        
        new_list = new_rmse_list(rmse_list = rmse, repeat_times = rmse_len)
        
        
        '''
        aud1 = columnplots[2][0]
        aud2 = columnplots[2][len(columnplots[2])-1]
        fillcolors = []
        for i in columnplots[1]:
            if i>=aud1 and i<=aud2:
                
                fillcolors.append('rgb(0,0,0)')
                
            else:
                fillcolors.append('rgba(54, 162, 235, 1)')
        fillcolors[0] = 'rgba(54, 162, 235, 1)'
        '''

        



        data = {
            'keyaud' : audplots[0],
            'keysr' : columnplots[0],
            'bigaud' : audplots[1],
            'bigsr' : columnplots[1],
            'search1aud' : audplots[2],
            'search1sr' : columnplots[2],
            'search2aud' : audplots[3],
            'search2sr' : columnplots[3],
            'search3aud' : audplots[4],
            'search3sr' : columnplots[4],
            'rmse': new_list,
            'lentime': lentime
            
                
        
        
        }
        
        return Response(data)


def new_rmse_list(rmse_list = [], repeat_times = 56):
    
    # declaring magnitude of repetition 
    K = repeat_times
    
    # using itertools.chain.from_iterable()  
    # + itertools.repeat() repeat elements K times 
    new_list = list(itertools.chain.from_iterable(itertools.repeat(i, K) for i in rmse_list)) 
        
    return new_list











"********************plot************************"

"================================================"

def get_chroma_features(sound_window = [], plot=True):
    y = sound_window
    
    # Compute chroma features from the harmonic signal
    chroma_cq = librosa.feature.chroma_cqt(y=y,
                                       sr=22050, hop_length= 512)
    
    if plot == True:
        
        librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time')
        plt.title('chroma_cqt')
        plt.colorbar()       
        plt.tight_layout()
        plt.show()

        for pitch_class in range(0,12):

            title_str = "Pitch Class: " + str(pitch_class)
            plt.figure(figsize=(17,5))
            plt.title(title_str)
            plt.plot(chroma_cq[pitch_class,:])
            plt.show()
    
    df1 = pd.DataFrame(chroma_cq).T.add_prefix('pitch_')
    
    return df1



def get_mel_spectrogram_features(sound_window = [], plot= True):       
    # rename window
    y = sound_window
    
    mel_spec = librosa.feature.melspectrogram(y=y, sr=22050)
    
    if plot == True:
        
        librosa.display.specshow(mel_spec, x_axis='time',y_axis='mel', sr=sr,fmax=8000)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')
        plt.tight_layout()
        plt.show()

        for freq in range(0,128):

            title_str = "Mel Class: " + str(freq)
            plt.figure(figsize=(17,5))
            plt.title(title_str)
            plt.plot(mel_spec[freq,:])
            plt.show()
    
    df1 = round(pd.DataFrame(mel_spec).T.add_prefix('mel_'),6)
    
    df2 = df1[['mel_0', 'mel_1', 'mel_2', 'mel_3', 'mel_4', 'mel_5', 'mel_6', 'mel_7',
       'mel_8', 'mel_9', 'mel_10', 'mel_11', 'mel_12', 'mel_13', 'mel_14',
       'mel_15', 'mel_16', 'mel_17', 'mel_18', 'mel_19', 'mel_20', 'mel_21',
       'mel_22', 'mel_23', 'mel_24', 'mel_25', 'mel_26', 'mel_27', 'mel_28',
       'mel_29', 'mel_30', 'mel_31', 'mel_32', 'mel_33', 'mel_34', 'mel_35',
       'mel_36', 'mel_37', 'mel_38', 'mel_39', 'mel_40', 'mel_41', 'mel_42',
       'mel_43', 'mel_44', 'mel_45', 'mel_46', 'mel_47', 'mel_48', 'mel_49',
       'mel_50', 'mel_51', 'mel_52', 'mel_53', 'mel_54', 'mel_55', 'mel_56',
       'mel_57', 'mel_58', 'mel_59', 'mel_60', 'mel_61', 'mel_62', 'mel_63',
       'mel_64', 'mel_65', 'mel_66', 'mel_67', 'mel_68', 'mel_69', 'mel_70',
       'mel_71', 'mel_72', 'mel_73', 'mel_74', 'mel_75', 'mel_76', 'mel_77',
       'mel_78', 'mel_79', 'mel_80', 'mel_81', 'mel_82', 'mel_83', 'mel_84',
       'mel_85', 'mel_86', 'mel_87', 'mel_88', 'mel_89', 'mel_90', 'mel_91',
       'mel_92', 'mel_93', 'mel_94', 'mel_95', 'mel_96', 'mel_97']]
    
    
    return df2


# target_audio, target_sr = librosa.load('Voice_042.wav')
#
    # len(target_audio)
# yt, index = librosa.effects.trim(target_audio, top_db=40)
# len(yt)
# mf_table = get_mel_spectrogram_features(sound_window = yt, plot= False)
# mf_table.describe().T.sort_values(by='50%', ascending=False)
# mf_table.describe().T.loc[~(mf_table.describe().T['50%'] == 0)].index



def get_zero_crossing_rate(sound_window = [], plot=True):
    
    # rename window
    y = sound_window
    
    cross_rate = librosa.feature.zero_crossing_rate(y=y)
    
    if plot == True:
        title_str = "Zero Crossing Rate"
        plt.figure(figsize=(17,5))
        plt.title(title_str)
        plt.plot(cross_rate[0,:])
        plt.show()
    
    df1 = pd.DataFrame(cross_rate).T.rename(columns={0:'Zero_Cross_Rate'})
    
    return df1


def get_features(sound_window = [], feature_name = 'chroma'):
    
    if feature_name == 'chroma':
        # get chroma features
        feature_df = get_chroma_features(sound_window = sound_window, plot=False)
        
    elif feature_name == 'melspec':
        # get mel spectrogram features
        feature_df = get_mel_spectrogram_features(sound_window = sound_window, plot=False)
    
    elif feature_name == 'zerocross':
        # get zero crossing rate
        feature_df = get_zero_crossing_rate(sound_window = sound_window, plot=False)
    
    # merge the dataframe
#     comb_df1 = pd.merge(chroma_cq_df, mel_spec_df, left_index= True, right_index=True, how='inner')
#     comb_df2 = pd.merge(comb_df1, zero_cross_df, left_index= True, right_index=True, how='inner')
    
#     print(comb_df2.shape)
    
    return feature_df



def compare_features(test_audio = [], target_audio = [], feature_name='melspec', plot=True):       
    start_time_seconds = time.time()
    
    window_size = len(target_audio)
    obj = Input_audios.objects.last()
    wsize = obj.window_size
    rmse_holder = []
    max_error_holder = []
    sample_holder = []
    # get features for the target audio
    feature_target = get_features(sound_window = target_audio, feature_name= feature_name)
    
    #for i in range(0, len(test_audio), window_size):
    for i in range(0, len(test_audio), wsize):
        
        test_set = test_audio[i:i+window_size]
        
        if len(test_set) == window_size:
            
            feature_test = get_features(sound_window = test_set, feature_name= feature_name)
            
            # calculate the rmse
            rmse = mean_squared_error(feature_target, feature_test, squared=False)
            rmse_holder.append(rmse)
            # calculate the max error score - on raw audio itself
            max_error_val = max_error(target_audio, test_set)
            max_error_holder.append(max_error_val)
            # append the sample holder
            sample_holder.append(i)
            
        elif len(test_set) < window_size:
            
            last_test_set = test_audio[-window_size:]
            
            feature_test = get_features(sound_window = last_test_set, feature_name= feature_name)
            
            # calculate the rmse
            rmse = mean_squared_error(feature_target, feature_test, squared=False)
            rmse_holder.append(rmse)
            # calculate the max error score - on raw audio itself
            max_error_val = max_error(target_audio, last_test_set)
            max_error_holder.append(max_error_val)
            # append the sample holder
            sample_holder.append(i)
            
        
    if plot == True:
        plt.figure(figsize=(17,5))
        plt.title('RMSE Graph')
        plt.plot(rmse_holder, color='teal');
        plt.show()
        plt.figure(figsize=(17,5))
        plt.title('Max Error Graph')
        plt.plot(max_error_holder, color='darkgoldenrod');
        plt.show()
        
    result_df = pd.DataFrame({'sample_loc': sample_holder, 'rmse': rmse_holder, 'max_error': max_error_holder})
    
    stop_time_seconds = time.time()
    runtime = round((stop_time_seconds - start_time_seconds),2)
    print('The feature extraction and comparison runtime of ', feature_name, ' is: ', runtime, ' seconds')
    return result_df, runtime


def cost_function(featureList=['melspec', 'chroma', 'zerocross'], coefficientValues= [0.9, 0.9, 0.8],
                  target_audio = [], test_audio=[], plot=True):
    print("d")
    
    # TODO -- iterate over the feature list and add results in the placeholder
    
    # when the feature name is melspec
    result_melspec, runtime_melspec = compare_features(test_audio = test_audio, target_audio = target_audio,
                                                       feature_name='melspec', plot=False)
    # when the feature name is melspec
    result_chroma, runtime_chroma = compare_features(test_audio = test_audio, target_audio = target_audio,
                                                       feature_name='chroma', plot=False)
    # when the feature name is melspec
    result_zerocross, runtime_zerocross = compare_features(test_audio = test_audio, target_audio = target_audio,
                                                       feature_name='zerocross', plot=False)
    
    # set index of result df at sample loc
    result_melspec2 = result_melspec.set_index('sample_loc')
    result_chroma2 = result_chroma.set_index('sample_loc')
    result_zerocross2 = result_zerocross.set_index('sample_loc')
    
    # set coefficients for each
    agg_df = result_melspec2 * coefficientValues[0] + result_chroma2 * coefficientValues[1] + \
                result_zerocross2 * coefficientValues[2]
    
    avg_df = agg_df / len(featureList)
    
    
    if plot == True:
        plt.figure(figsize=(17,5))
        plt.title('RMSE Graph')
        plt.plot(avg_df['rmse'], color='teal');
        plt.show()
        plt.figure(figsize=(17,5))
        plt.title('Max Error Graph')
        plt.plot(avg_df['max_error'], color='darkgoldenrod');
        plt.show()
    print(avg_df.head(5))
    
    return avg_df


def evaluate_comparison(result_df = pd.DataFrame(), rmse_threshold = 10, max_error_threshold = 0.20):
    print("e")
    
    result_df = result_df.reset_index()
    # sort the result with min rmse and max error
    sorted_df = result_df.sort_values(by=['rmse', 'max_error'], ascending=[True, True])
    
    # find the sample loc of the min rmse and min of max error
    start_loc = sorted_df['sample_loc'].iloc[0]
    selected_rmse = sorted_df['rmse'].iloc[0]
    selected_max_error = sorted_df['max_error'].iloc[0]
    
    
    # if the rmse and max error are below certain threshold
    if (selected_rmse < rmse_threshold) and (selected_max_error < max_error_threshold):
    
        # Print
        print('The target audio clip has potentially been found')
        print('The target audio starts at: ', start_loc, ' sample')
        print('The RMSE of the sample is : ', selected_rmse)
        print('The Max Error of the sample is : ', selected_max_error)
        
    else:
        print('The target audio clip could not be found')
        
    return sorted_df


def trim_resample_average(sample_1_file='abc.wav', sample_2_file='def.wav', sample_3_file='ghi.wav'):
    print("c")  
    # read the file and get timeseries
    raw_y1, sr1 = librosa.load(sample_1_file, sr= 22050)
    raw_y2, sr2 = librosa.load(sample_2_file, sr= 22050)
    raw_y3, sr3 = librosa.load(sample_3_file, sr= 22050)
    
    # trim the start and end silence
    y1, index1 = librosa.effects.trim(raw_y1, top_db=35)
    y2, index2 = librosa.effects.trim(raw_y2, top_db=35)
    y3, index3 = librosa.effects.trim(raw_y3, top_db=35)
    
    # calculate the mean length of the time series
    avg_length = np.mean([len(y1), len(y2), len(y3)])
    
    # determine the new sampling rate adjusted for the average length
    time_duration_1 = len(y1) / sr1
    new_sr1 = avg_length / time_duration_1
    
    time_duration_2 = len(y2) / sr2
    new_sr2 = avg_length / time_duration_2
    
    time_duration_3 = len(y3) / sr3
    new_sr3 = avg_length / time_duration_3
    
    # resample the audio signals with new sampling rate
    adj_y1 = librosa.resample(y1, sr1, new_sr1)
    adj_y2 = librosa.resample(y2, sr2, new_sr2)
    adj_y3 = librosa.resample(y3, sr3, new_sr3)
    
    # calculate the mean of the adjusted sampling rate
    mean_new_sr = np.mean([new_sr1, new_sr2, new_sr3])
    
    # calculate the mean of three audio time series
    mean_new_y = np.mean([adj_y1, adj_y2, adj_y3], axis=0)
    
    # return mean y and mean sr
    return mean_new_y, mean_new_sr



def write_audio_output(keyword, potential_df = pd.DataFrame(), target_length = 10.0, test_audio=[], test_sr=10.0):
    word = keyword
    output = Output_audios()
    out_file_list = []
    output.keyword = word
    
    rmseval = list(potential_df.sort_index()['rmse'])
    '''
    rmse_list = list(potential_df.sort_index()['rmse'])
    print(rmse_list)
    plt.figure(figsize=(17,5))
    plt.title('RMSE Graph')
    plt.plot(rmse_list, color='darkgoldenrod')
    plt.savefig('E:\\Freelance\\rmse.jpg')

    rmse_list_expanded = new_rmse_list(rmse_list = rmse_list, repeat_times = 56)
    '''
    output.rmse = rmseval
    
    # convert the first search result into audio
    start_point = potential_df['sample_loc'].iloc[0]
    end_point = start_point + target_length
    audio_subset = test_audio[start_point: end_point]
    output.start_time = start_point
    output.end_time = end_point

    current_time = datetime.datetime.now()
    timestr = str(current_time.year) + "_" + str(current_time.month) + "_" + str(current_time.day) + "_" + str(current_time.hour) + "_" + str(current_time.minute) + "_" + str(current_time.second)
    timesave1 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\search_1" + timestr
    librosa.output.write_wav(timesave1, audio_subset, sr=test_sr)
    out_file_list.append(timesave1)
    
    output.search_1 = "media/search_1" + timestr
    
    #search = open('C:\\Users\\PSSRE\\Djangoproject\\Freelance\\search_1.wav','r')
    #output_list.append(search)
    
    #audio_output.search_1 = wave.open('C:\\Users\\PSSRE\\Djangoproject\\Freelance\\search_1.wav')
    
    # convert the second search result into audio
    start_point = potential_df['sample_loc'].iloc[1]
    end_point = start_point + target_length
    audio_subset = test_audio[start_point: end_point]
    timesave2 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\search_2" + timestr
    librosa.output.write_wav(timesave2, audio_subset, sr=test_sr)
    output.search_2 = "media/search_2" + timestr
    out_file_list.append(timesave2)
    
    # convert the third search result into audio
    start_point = potential_df['sample_loc'].iloc[2]
    end_point = start_point + target_length
    audio_subset = test_audio[start_point: end_point]
    timesave3 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\search_3" + timestr
    librosa.output.write_wav(timesave3, audio_subset, sr=test_sr)
    output.search_3 = "media/search_3" + timestr
    out_file_list.append(timesave3)
    
    # convert the fourth search result into audio
    start_point = potential_df['sample_loc'].iloc[3]
    end_point = start_point + target_length
    audio_subset = test_audio[start_point: end_point]
    timesave4 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\search_4" + timestr
    librosa.output.write_wav(timesave4, audio_subset, sr=test_sr)
    output.search_4 = "media/search_4" + timestr
    out_file_list.append(timesave4)
    
    # convert the fifth search result into audio
    start_point = potential_df['sample_loc'].iloc[4]
    end_point = start_point + target_length
    audio_subset = test_audio[start_point: end_point]
    timesave5 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\search_5" + timestr
    librosa.output.write_wav(timesave5, audio_subset, sr=test_sr)
    output.search_5 = "media/search_5" + timestr
    out_file_list.append(timesave5)
    
    # convert the fifth search result into audio
    start_point = potential_df['sample_loc'].iloc[5]
    end_point = start_point + target_length
    audio_subset = test_audio[start_point: end_point]
    timesave6 = "C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Audio_project\\Audio_analyser\\media\\media\\search_6" + timestr
    librosa.output.write_wav(timesave6, audio_subset, sr=test_sr)
    output.search_6 = "media/search_6" + timestr
    out_file_list.append(timesave6)
    

    visual_files = []
    for i in out_file_list:
        visual_files.append(visualisation(i,2))
    output.visual_1 = visual_files[0]
    output.visual_2 = visual_files[1]
    output.visual_3 = visual_files[2]
    output.visual_4 = visual_files[3]
    output.visual_5 = visual_files[4]
    output.visual_6 = visual_files[5]
    output.runtime = 0
    
    output.save()
    return timesave1,timesave2,timesave3,timesave4,timesave5,timesave6
    


def search_function(malspec, chroma, zerocross, sdf, keyword, keyword_file1= 'abc.wav', keyword_file2='def.wav', keyword_file3 = 'ghi.wav',
                    large_audio_file='xyz.wav'):
    n_keyword = keyword 
    start_time_seconds = time.time()
    target_audio, target_sr = trim_resample_average(sample_1_file=keyword_file1,
                                                    sample_2_file=keyword_file2, sample_3_file=keyword_file3)
    
    
    target_audio, target_sr = librosa.load(keyword_file1)
    
    
    target_audio, index = librosa.effects.trim(target_audio, top_db=sdf)
    
    test_filename = large_audio_file
    
    test_audio, test_sr = librosa.load(test_filename, sr= target_sr)
    testfile = test_audio.tolist()
    
    result = cost_function(featureList=['malspec', 'chroma', 'zerocross'],
                       coefficientValues= [malspec, chroma , zerocross], 
                       target_audio = target_audio,
                        test_audio = test_audio,
#                       test_audio=test_audio[int(test_sr*2):-int(test_sr*2)],
                       plot=False)
    
    potential_df = evaluate_comparison(result_df = result, rmse_threshold = 7, max_error_threshold = 0.70)
    
    
    
    # store the output in audio form
    file_list = write_audio_output(keyword = n_keyword, potential_df = potential_df, target_length = len(target_audio),
                       test_audio=test_audio, test_sr=int(test_sr))

    #calculating runtime of whole process
    stop_time_seconds = time.time()
    runtime = round((stop_time_seconds - start_time_seconds),2)
    obj = Output_audios.objects.last()
    obj.runtime = runtime
    obj.test_audio = testfile
    #obj.start_time = potential_df['sample_loc'].iloc[0]
    
    #obj.end_time = potential_df['sample_loc'].iloc[0] + len(target_audio)
    obj.save()

    plotobj = Plotter.objects.last()
    plotobj.runtime = runtime
    plotobj.save()

   


    

    
    return potential_df, file_list


#search_function(keyword_file1= 'C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Voice_042.wav', keyword_file2='C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Voice 043.wav', keyword_file3 = 'C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Voice 044.wav',
                #    large_audio_file='C:\\Users\\PSSRE\\Djangoproject\\Freelance\\Voice 045.wav')

