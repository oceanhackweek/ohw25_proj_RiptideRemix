# mixer/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import os
import json
from django.conf import settings
import traceback

# Import spectrogram utilities
try:
    from .spectrogram_utils import generate_spectrogram as generate_spectrogram_util
    from .spectrogram_utils import get_audio_file_path
    SPECTROGRAM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import spectrogram utilities: {e}")
    SPECTROGRAM_AVAILABLE = False
    # Define placeholder functions
    def generate_spectrogram_util(audio_path, speed, pitch, amplitude):
        return None

    def get_audio_file_path(audio_url):
        raise FileNotFoundError(f"Spectrogram utilities not available: {audio_url}")


class MixerView(TemplateView):
    template_name = "mixer/mixer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sound_structure = self.get_sound_structure()

        context['sound_structure'] = sound_structure
        context['sound_structure_json'] = sound_structure
        return context

    def get_sound_structure(self):
        # Try multiple possible locations
        possible_paths = [
            os.path.join(settings.BASE_DIR, 'static', 'sounds'),
            os.path.join(settings.BASE_DIR, 'static/sounds'),
            os.path.join('static', 'sounds'),
            'static/sounds',
            os.path.join(settings.STATIC_ROOT, 'sounds') if settings.STATIC_ROOT else None,
        ]

        sounds_path = None
        for path in possible_paths:
            if path and os.path.exists(path):
                sounds_path = path
                print(f"Found sounds at: {sounds_path}")
                break

        if not sounds_path:
            print("ERROR: Could not find sounds directory!")
            return

        sound_structure = {}

        try:
            items = os.listdir(sounds_path)
            for item in sorted(items):
                item_path = os.path.join(sounds_path, item)

                if os.path.isdir(item_path) and not item.startswith('.'):
                    sound_structure[item] = {}

                    # Process this category
                    self.process_category(item, item_path, sound_structure)

        except Exception as e:
            print(f"Error loading sound structure: {e}")
            import traceback
            traceback.print_exc()

        return sound_structure

    def process_category(self, category_name, category_path, sound_structure):
        try:
            for item in sorted(os.listdir(category_path)):
                item_path = os.path.join(category_path, item)

                if os.path.isdir(item_path) and not item.startswith('.'):
                    sound_structure[category_name][item] = {}
                    self.process_subcategory(category_name, item, item_path, sound_structure)
                elif item.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    print(f"  Found direct audio file: {item}")
                    if '_files' not in sound_structure[category_name]:
                        sound_structure[category_name]['_files'] = []
                    sound_structure[category_name]['_files'].append({
                        'filename': item,
                        'display_name': os.path.splitext(item)[0].replace('_', ' ').title(),
                        'url': f'/static/sounds/{category_name}/{item}'
                    })

        except Exception as e:
            print(f"Error processing category {category_name}: {e}")

    def process_subcategory(self, category_name, subcategory_name, subcategory_path, sound_structure):
        try:
            for item in sorted(os.listdir(subcategory_path)):
                item_path = os.path.join(subcategory_path, item)

                if os.path.isdir(item_path) and not item.startswith('.'):
                    sound_structure[category_name][subcategory_name][item] = []
                    self.process_species(category_name, subcategory_name, item, item_path, sound_structure)
                elif item.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    if '_files' not in sound_structure[category_name][subcategory_name]:
                        sound_structure[category_name][subcategory_name]['_files'] = []
                    sound_structure[category_name][subcategory_name]['_files'].append({
                        'filename': item,
                        'display_name': os.path.splitext(item)[0].replace('_', ' ').title(),
                        'url': f'/static/sounds/{category_name}/{subcategory_name}/{item}'
                    })

        except Exception as e:
            print(f"Error processing subcategory {subcategory_name}: {e}")

    def process_species(self, category_name, subcategory_name, species_name, species_path, sound_structure):
        try:
            audio_files = []
            for item in sorted(os.listdir(species_path)):
                if item.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    audio_files.append({
                        'filename': item,
                        'display_name': os.path.splitext(item)[0].replace('_', ' ').title(),
                        'url': f'/static/sounds/{category_name}/{subcategory_name}/{species_name}/{item}'
                    })

            sound_structure[category_name][subcategory_name][species_name] = audio_files

        except Exception as e:
            print(f"Error processing species {species_name}: {e}")


def generate_spectrogram_view(request):
    if not SPECTROGRAM_AVAILABLE:
        return JsonResponse({
            'success': False,
            'error': 'Spectrogram utilities not available. Check server logs.'
        }, status=500)

    if request.method == 'GET':
        audio_url = request.GET.get('audio_url', '')
        speed = float(request.GET.get('speed', 1.0))
        pitch = int(request.GET.get('pitch', 0))
        amplitude = float(request.GET.get('amplitude', 1.0))

        print(f"Parameters: audio_url={audio_url}, speed={speed}, pitch={pitch}, amplitude={amplitude}")

        if not audio_url:
            return JsonResponse({'error': 'No audio URL provided'}, status=400)

        try:
            # Get the actual file path
            audio_path = get_audio_file_path(audio_url)
            print(f"Found audio file at: {audio_path}")

            # Generate the spectrogram using the UTILITY function
            spec_base64 = generate_spectrogram_util(audio_path, speed, pitch, amplitude)

            if spec_base64 is None:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to generate spectrogram'
                }, status=500)

            return JsonResponse({
                'success': True,
                'spectrogram': spec_base64,
                'audio_url': audio_url
            })

        except FileNotFoundError as e:
            print(f"File not found error: {e}")
            return JsonResponse({
                'success': False,
                'error': f"Audio file not found: {audio_url}"
            }, status=404)
        except Exception as e:
            print(f"Unexpected error: {e}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
