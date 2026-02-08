## <img src="https://github.com/oceanhackweek/ohw25_proj_RiptideRemix/blob/main/staticfiles/Images/logo.png" alt="Logo" width="50" height="50">  RiptideRemix
This repository hosts the source code for an OceanHackWeek2025 project to allow for audio classificaiton and audio-synthesis of acoustic soundsources. 

https://riptide-remix-ac6c13c5a06d.herokuapp.com

https://riptide-remix.onrender.com/

## Collaborators

| Name                  | Role                |
|-----------------------|---------------------|
| Kasey Castello        | Web page designing / Educational Materials / Acoustic Processing         |
| Mattie Toll           | Bioacoustic processing / Machine Learning         |
| Oluwatofunmi Adeboye  | Seismic guru         |
| Isabelle Brandicourt  | Acoustic processing / mixing / data sourcing         |
| Derya Gumustel        | Web page designing              |
| Dwight Owens          | Mentor              |

## Planning

* Initial idea: "Acoustic mixer like GarageBand but pulling from oceanographic databases and processing data locally to pull out key sound bites."
* Slack channel: ohw25_proj_riptideremix
* Project google drive: [Add link](https://drive.google.com/drive/u/0/folders/1ZIcpZ1LWX_HtODz82-y-NJ0_Y0PhGG8u)
* Presentation: [Add link](https://docs.google.com/presentation/d/1SlbmSwNPd_eR4nL1RnYAX1_k1MJDHnvv7haCEPxDIH8/edit?slide=id.p#slide=id.p)

## Background
This project was driven from simple question: What if we could turn the rhythms of the Earth into music? Maybe having a toolbox like a GarageBand, combining acoustic data science, seismic waves, and adding a touch of creativity, we’ve built a framework for an interactive dashboard that invites users to explore, list and remixes the sounds of the ocean. Using real geophysical and marine datasets, anyone can create new compositions by dragging, adjusting, and layering natural sounds into immersive sonic experiences. The idea is both playful and educational: bridging the gap between raw scientific data and artistic expression, while providing users with meaningful insights into the Earth’s dynamic systems. This will also a great toolbox for science education especially for highschool.

## Goals
The goals are to;
* Create an intuitive tool for remixing oceanic and seismic audio data into custom soundscapes.
* Introduce scientific literacy through interactive sonification—turning seismic and marine events into audible experiences.
* Highlight real datasets and their sources, including the hardware and environments behind the recordings.
* Visualize waveforms and spectrograms in a way that’s informative for researchers and captivating for the public.

## Datasets
We use a curated collection of publicly available acoustic and geophysical datasets. These include:
* Ocean Networks Canada (ONC) – Hydrophone and oceanographic sensor data from the deep sea.
* NSF’s SAGE Facility – Seismic data from stations across the globe.
* OrcaSound – Real-time and archived orca calls and ambient marine audio.
* National Center for Environmental Information (NCEI) – Archived environmental and geophysical data.
* IRIS (Incorporated Research Institutions for Seismology) – Comprehensive seismic event data.
  
## Workflow/Roadmap
What’s working now:
* An interactive audio dashboard for remixing ocean sounds.
* Users can drag audio clips into a visual mixer and adjust pitch, speed, loop behavior, and more.
* Each composition is rendered as a waveform and spectrogram, providing both sonic and scientific views.
* A “sound map” is generated upon song completion, showing the origins and diversity of sounds used.
* Educational overlays explain sensor types, data sources, and waveform basics—bridging science and sound.

Earthquake Viewer and Soundscape Explorer:
* We’re now expanding into major seismic events, transforming global earthquakes into multi-sensory experiences:
* Visualize and hear waveforms from major events like:
* Japan 2011 (Mw 9.1), off-coast Alaska 2021 (Mw 8.2) and Russia 2025 (Mw 8.4)
* We apply standard preprocessing: demeaning, removing instrument responses, and filtering.
* Listen to seismic waves as they travel around the world—P-waves, S-waves, SKS into audible form.

In progress / Coming soon:
* Enhanced accessibility for educators and outreach professionals.
* Open API for artists and developers to contribute sound packs and compositions.\
* Full integration of station-event mapping with rose diagrams and waveform overlays.
* Feature to stack and compare waveforms from multiple stations or events.

