from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "riptideremix/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Up to 10 unique songs
        context['songs'] = [
            {"file": "my_final_song.wav", "img": "1.jpg", "title": "Our First Song", "author": "The Riptide Team"},
            {"file": "kasey_song.wav", "img": "2.jpg", "title": "Crush Depth", "author": "Kasey C."},
            {"file": "elliot_song.wav", "img": "3.jpg", "title": "Airgunz", "author": "Elliot C."},
            {"file": "Lil_Wayve.wav", "img": "4.jpg", "title": "Lil_Wayve", "author": "Aaron S."},
            {"file": "my_final_song.wav", "img": "5.jpg", "title": "Cool Song 5", "author": "The Riptide Team"},
            {"file": "my_final_song.wav", "img": "6.jpg", "title": "Cool Song 6", "author": "The Riptide Team"},
            {"file": "my_final_song.wav", "img": "7.jpg", "title": "Cool Song 7", "author": "The Riptide Team"},
            {"file": "my_final_song.wav", "img": "8.jpg", "title": "Cool Song 8", "author": "The Riptide Team"},
            {"file": "my_final_song.wav", "img": "9.jpg", "title": "Cool Song 9", "author": "The Riptide Team"},
            {"file": "my_final_song.wav", "img": "10.jpg", "title": "Cool Song 10", "author": "The Riptide Team"},
            # add more unique songs up to 10
        ][:10]  # limit to 10
        return context  # must be inside the method

class LearnView(TemplateView):
    template_name = "learn/learn_base.html"