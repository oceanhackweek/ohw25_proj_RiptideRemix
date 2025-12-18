# mixer/urls.py
from django.urls import path
from .views import MixerView, generate_spectrogram_view

urlpatterns = [
    path('', MixerView.as_view(), name='mixer'),
    path('spectrogram/', generate_spectrogram_view, name='generate_spectrogram'),
]

print("DEBUG: URLs loaded successfully")