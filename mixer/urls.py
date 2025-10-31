from django.urls import path
from .views import MixerView

urlpatterns = [
    path('', MixerView.as_view(), name='mixer'),
]
