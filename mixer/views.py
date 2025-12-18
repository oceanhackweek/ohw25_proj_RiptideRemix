from django.shortcuts import render
from django.views.generic import TemplateView
import os
from django.conf import settings
import json


class MixerView(TemplateView):
    template_name = "mixer/mixer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sound_structure = self.get_sound_structure()
        
        # Debug: Print structure to console
        print("=" * 50)
        print("SOUND STRUCTURE DEBUG:")
        print(f"Base directory: {settings.BASE_DIR}")
        print(f"Static directory: {os.path.join(settings.BASE_DIR, 'static')}")
        print(f"Sounds path: {os.path.join(settings.BASE_DIR, 'static', 'sounds')}")
        print(f"Path exists: {os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'sounds'))}")
        print(f"Number of categories found: {len(sound_structure)}")
        
        for category, content in sound_structure.items():
            print(f"\nCategory: {category}")
            if isinstance(content, dict):
                print(f"  Subcategories: {list(content.keys())}")
                for subcat, subcontent in content.items():
                    print(f"    Subcategory: {subcat}")
                    if isinstance(subcontent, dict):
                        print(f"      Items: {list(subcontent.keys())}")
        
        print("=" * 50)
        
        context['sound_structure'] = sound_structure
        context['sound_structure_json'] = json.dumps(sound_structure)
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
            print("Checked paths:", possible_paths)
            # Create a dummy structure for testing
            return {
                'Anthropogenic': {
                    '_files': [
                        {
                            'filename': 'test.wav',
                            'display_name': 'Test Sound',
                            'url': '/static/sounds/test.wav'
                        }
                    ]
                },
                'Biological': {
                    'Cetacean': {
                        'Mysticetes': {
                            'HumpbackWhale': [
                                {
                                    'filename': 'test_humpback.wav',
                                    'display_name': 'Test Humpback',
                                    'url': '/static/sounds/test.wav'
                                }
                            ]
                        }
                    }
                },
                'Other': {
                    '_files': [
                        {
                            'filename': 'ice_cracking.wav',
                            'display_name': 'Ice Cracking',
                            'url': '/static/sounds/Other/ice_cracking.wav'
                        }
                    ]
                },
                'Seismic': {
                    'Alaska2021': {
                        '_files': [
                            {
                                'filename': 'quake_audio.wav',
                                'display_name': 'Quake Audio',
                                'url': '/static/sounds/Seismic/Alaska2021/quake_audio.wav'
                            }
                        ]
                    }
                }
            }
        
        sound_structure = {}
        
        try:
            # List all items in sounds directory
            items = os.listdir(sounds_path)
            print(f"Items in sounds directory: {items}")
            
            for item in sorted(items):
                item_path = os.path.join(sounds_path, item)
                
                if os.path.isdir(item_path) and not item.startswith('.'):
                    print(f"\nProcessing category: {item}")
                    sound_structure[item] = {}
                    
                    # Process this category
                    self.process_category(item, item_path, sound_structure)
        
        except Exception as e:
            print(f"Error loading sound structure: {e}")
            import traceback
            traceback.print_exc()
        
        return sound_structure
    
    def process_category(self, category_name, category_path, sound_structure):
        """Process a category directory"""
        try:
            for item in sorted(os.listdir(category_path)):
                item_path = os.path.join(category_path, item)
                
                if os.path.isdir(item_path) and not item.startswith('.'):
                    # This is a subcategory
                    print(f"  Found subcategory: {item}")
                    sound_structure[category_name][item] = {}
                    self.process_subcategory(category_name, item, item_path, sound_structure)
                elif item.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    # This is a direct audio file in category
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
        """Process a subcategory directory"""
        try:
            for item in sorted(os.listdir(subcategory_path)):
                item_path = os.path.join(subcategory_path, item)
                
                if os.path.isdir(item_path) and not item.startswith('.'):
                    # This is a species directory
                    print(f"    Found species: {item}")
                    sound_structure[category_name][subcategory_name][item] = []
                    self.process_species(category_name, subcategory_name, item, item_path, sound_structure)
                elif item.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    # This is a direct audio file in subcategory
                    print(f"    Found audio file in subcategory: {item}")
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
        """Process a species directory"""
        try:
            audio_files = []
            print(f"      Processing species directory: {species_path}")
            for item in sorted(os.listdir(species_path)):
                if item.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    print(f"        Found audio file: {item}")
                    audio_files.append({
                        'filename': item,
                        'display_name': os.path.splitext(item)[0].replace('_', ' ').title(),
                        'url': f'/static/sounds/{category_name}/{subcategory_name}/{species_name}/{item}'
                    })
            
            sound_structure[category_name][subcategory_name][species_name] = audio_files
        
        except Exception as e:
            print(f"Error processing species {species_name}: {e}")