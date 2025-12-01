"""
URL configuration for riptideremix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import HomeView, LearnView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('learn/', LearnView.as_view(), name='learn'),
    path('mixer/', include('mixer.urls')),
    path('data/', TemplateView.as_view(template_name='riptideremix/data.html'), name='data'),
    path('education/', TemplateView.as_view(template_name='riptideremix/education.html'), name='education'),
    path('about/', TemplateView.as_view(template_name='riptideremix/about.html'), name='about'),
    path('gallery/', TemplateView.as_view(template_name='riptideremix/gallery.html'), name='gallery'),
    path('admin/', admin.site.urls),
]
