from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "riptideremix/home.html"

class LearnView(TemplateView):
    template_name = "learn/learn_base.html"
