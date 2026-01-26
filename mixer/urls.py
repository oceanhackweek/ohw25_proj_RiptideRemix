# mixer/urls.py
from django.urls import path
from .views import MixerView, generate_spectrogram_view, spectrogram_view, timeseries_view
from . import views

urlpatterns = [
    path('', MixerView.as_view(), name='mixer'),
    path('spectrogram/', views.spectrogram_view, name='generate_spectrogram'),
    path('timeseries/', timeseries_view, name='timeseries'),
]

print("DEBUG: URLs loaded successfully")
