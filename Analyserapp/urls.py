from django.contrib import admin
from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('upload', views.file_upload, name='file_upload'),
    path('results',views.result_page,name='result_fetch'),
    path('datasubmit',views.datasubmit,name='datasubmit'),
    path('search_keyword',views.search, name='search'),
    path('plotter',views.plotter,name='plotter'),
    path('plot/',views.Chartdata.as_view(),name='plot'),
    path('chart',views.chart,name="chart"),
    path('jschart',views.jsaudio,name="jsaudio"),
    path('resultplot1',views.Resultplot1.as_view(),name="resultplot1"),
    path('searchplot',views.Searchplot.as_view(),name='searchplot'),
    path('defresults',views.Defresults.as_view(),name="defresults")
]

urlpatterns = urlpatterns+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)