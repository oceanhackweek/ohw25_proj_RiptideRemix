import marimo

__generated_with = "0.14.17"
app = marimo.App(
    width="columns",
    app_title="RiptideRemix_mixer",
    layout_file="layouts/visualize_quakes.grid.json",
)


@app.cell(column=0)
def _():
    import platform
    from pathlib import Path

    # Detect OS and set project root accordingly
    if platform.system() == "Windows":
        basePath = Path("C:/Users/kasey/Desktop/ohw25_proj_RiptideRemix")
    else:
        basePath = Path("/home/jovyan/ohw25_proj_RiptideRemix")
    return (basePath,)


@app.cell
def _(basePath):
    import marimo as mo
    mo.image(
        src= basePath / "Images" / "logo_flat.jpg",
        alt="placeholder",
        width=1200,
        height=100,
        rounded=True,
        caption=""
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Hey there! Welcome to your data playground! Here, you can dive into different datasets and discover how researchers pick the perfect spots to study. Check out the “Seismic” and “Hydrophone” sections below to start exploring our data.""")
    return


@app.cell
def _(mo):
    mo.md("""---""")
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" /  "ArtGifs" / "placeholder.gif",
        alt="placeholder",
        width=900,
        height=200,
        rounded=False,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md("""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "welcome.png",
        alt="placeholder",
        width=115,
        height=115,
        rounded=False,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell(column=1)
def _(mo):
    nav_menu = mo.nav_menu({
        "/": "Mix Sounds",  # internal
        "/learn": "Learn More",  # internal
        "/about": "About the Team",  # internal
        "/quake": "Gather More Data"
    })
    nav_menu
    return


@app.cell(column=2)
def _(mo):
    mo.md(r"""Scientists use Ocean Bottom Seismometers (OBS) to measure vibrations in the seafloor, monitor earthquakes, and study the movement of Earth beneath the ocean. This helps researchers understand geological processes in ways that aren’t visible from the surface. In this interface, anyone can look at the data through these seismic waveforms produced from different Earthquakes.""")
    return


@app.cell
def _(mo):
    mo.md(r"""### Choose Your Clip:""")
    return


@app.cell
def _(UTCDateTime):

    big_events = { "Japan_2011": { "start_time": UTCDateTime("2011-03-11T05:46:23"),
                                  "latitude": 38.297, "longitude": 142.372, "depth_km": 29
                                 },
                   "Alaska_2021": { "start_time": UTCDateTime("2021-07-29T06:15:49"),
                                    "latitude": 55.325,"longitude": -157.972, "depth_km": 32
                                  },
                   "Russia_2025": {"start_time": UTCDateTime("2025-07-25T00:15:30"),
                                   "latitude": 54.000, "longitude": 160.0000, "depth_km": 25
                                  }
                }
    return (big_events,)


@app.cell
def _(selected_network, selected_station):
    station_info = {
        "station": selected_station,
        "network": selected_network
    }
    return (station_info,)


@app.cell
def _(mo):
    mo.md(r"""Earthquake:""")
    return


@app.cell
def _(mo):
    earthquake_dropdown = mo.ui.dropdown(options={'Japan_2011': 1, 'Alaska_2021': 2, 'Russia_2025': 3}, value = 'Japan_2011')
    return (earthquake_dropdown,)


@app.cell
def _(earthquake_dropdown):
    earthquake_dropdown
    return


@app.cell
def _(mo):
    mo.md(r"""Network:""")
    return


@app.cell
def _(mo):
    network_dropdown = mo.ui.dropdown(options={'AF': 1, 'AU': 2, 'G': 3, 'IM': 4, 'IP': 5, 'IU': 6, 'NJ': 7, 'NZ': 8}, value = 'AF')
    return (network_dropdown,)


@app.cell
def _(network_dropdown):
    network_dropdown
    return


@app.cell
def _(mo):
    mo.md(r"""Station:""")
    return


@app.cell
def _(mo, network_dropdown):
    if network_dropdown.selected_key == "AF":
        statOpts = ["AAUS", "ANKE", "DESE", "EKNA", "IFE", "KAD", "NSU"]
    elif network_dropdown.selected_key == "AU":
        statOpts = ["MCQ"]
    elif network_dropdown.selected_key == "G":
        statOpts = ["MCQ"]
    elif network_dropdown.selected_key == "IM":
        statOpts = ["MCQ"]
    elif network_dropdown.selected_key == "IP":
        statOpts = ["MCQ"]
    elif network_dropdown.selected_key == "IU":
        statOpts = ["MCQ"]
    elif network_dropdown.selected_key == "NJ":
        statOpts = ["MCQ"]
    elif network_dropdown.selected_key == "NZ":
        statOpts = ["MCQ"]
    else:
        statOpts = []

    station_dropdown = mo.ui.dropdown(options=statOpts)
    return (station_dropdown,)


@app.cell
def _(station_dropdown):
    station_dropdown
    return


@app.cell
def _(mo):
    mo.md(r"""Channel:""")
    return


@app.cell
def _(mo):
    channel_dropdown = mo.ui.dropdown(options={'BH1': 1, 'BH2': 2, 'BHZ': 3}, value = 'BH1')
    return (channel_dropdown,)


@app.cell
def _(channel_dropdown):
    channel_dropdown
    return


@app.cell
def _(mo):
    mo.md(r"""Filter:""")
    return


@app.cell
def _(mo):
    filter_ranges = { "0.01 - 0.10 Hz": (0.01, 0.10), "0.05 - 0.20 Hz": (0.05, 0.20), "0.01 - 0.50 Hz": (0.01, 0.50), "0.03 - 0.10 Hz": (0.03, 0.10), "0.03 - 0.15 Hz": (0.03, 0.15) }

    filter_dropdown = mo.ui.dropdown(options=list(filter_ranges.keys()))
    return filter_dropdown, filter_ranges


@app.cell
def _(filter_dropdown):
    filter_dropdown
    return


@app.cell(column=3)
def _(mo):
    mo.md(r"""## Seismogram from Ocean Bottom Seismometers (OBS)""")
    return


@app.cell
def _():
    import obspy as os
    import obspy.signal
    from obspy.clients.fdsn import Client
    from obspy import clients
    from obspy import UTCDateTime
    import matplotlib.pyplot as plt
    from obspy.taup import TauPyModel
    from obspy.geodetics import locations2degrees
    from scipy.io import wavfile
    import IPython.display as ipd
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import random
    from scipy.signal import spectrogram
    import numpy as np
    return (
        Client,
        TauPyModel,
        UTCDateTime,
        ccrs,
        cfeature,
        locations2degrees,
        np,
        plt,
        random,
        spectrogram,
    )


@app.cell
def _(
    Client,
    TauPyModel,
    big_events,
    channel_dropdown,
    earthquake_dropdown,
    locations2degrees,
    network_dropdown,
    station_dropdown,
):
    client = Client('IRIS')
    model = TauPyModel(model = "ak135")      # In the dropdown menu we can have models using either models "iasp91", "ak135", "ak135f", "prem"


    selected_event = earthquake_dropdown.selected_key
    selected_network = network_dropdown.selected_key       #I don't know how this will be connected to networ_stations, i don't know how
    selected_station = station_dropdown.selected_key
    selected_channel = channel_dropdown.selected_key      # We can have a drop down for three channels(BH1, BH2, BHZ), for now maybe just
    selected_location = "*"        # Thwill serve as a wildcat (*), you can use various wildcat tho in the drop down,
                                   # eg BH?, LH?

    event = big_events[selected_event]
    start_time = event["start_time"]
    end_time = start_time + 10000
    event_lat = event["latitude"]
    event_lon = event["longitude"]
    event_depth_km = event["depth_km"]

    try:
        st = client.get_waveforms(selected_network, selected_station, selected_location,
                                  selected_channel, start_time, end_time, attach_response=True
                                 )
        st_rem = st.copy()
        st_rem.remove_response(output="VEL")
        st_rem.detrend('linear')
        st_rem.detrend('demean')
        tr = st_rem[0]

        inv = client.get_stations( network=selected_network, station=selected_station,
                               level="station", starttime=start_time, endtime=end_time
                             )
        sta = inv[0][0]
        station_lat = sta.latitude
        station_lon = sta.longitude
        distance_deg = locations2degrees(event_lat, event_lon, station_lat, station_lon)
    except Exception as e:
        print(f"There was a download error, please check inputs Maybe incorrect channel, station and network name Ensure your input is correct and well written: {e}")
    return (
        distance_deg,
        event_depth_km,
        event_lat,
        event_lon,
        model,
        selected_channel,
        selected_event,
        selected_network,
        selected_station,
        station_lat,
        station_lon,
        tr,
    )


@app.cell
def _():
    phase_types = ["P", "S", "SKS", "SKKS"]
                                                        #This part shows the TauP phases we wanna overlay on the plots
                                                        # What this does that is shows the body waves(P&S) arrival amongst others
    arrival_colors = {'P': 'r',
                      'S': 'g',
                      'SKS': 'b',
                      'SKKS': 'm'}

    colors = [
                'k', 'r', 'b', 'g',
                'orange','purple',
                'cyan','magenta'
            ]
    return arrival_colors, colors, phase_types


@app.cell
def _(
    event_lat,
    event_lon,
    plot_event_station_map,
    station_info,
    station_lat,
    station_lon,
):
    import warnings
    warnings.simplefilter("ignore")
    fig4 = plot_event_station_map(event_lat, event_lon, station_lat, station_lon, station_info)
    return (fig4,)


@app.cell
def _(fig4):
    fig4
    return


@app.cell
def _(
    arrival_colors,
    colors,
    distance_deg,
    event_depth_km,
    filter_dropdown,
    filter_ranges,
    model,
    phase_types,
    plt,
    random,
    selected_channel,
    selected_event,
    selected_network,
    selected_station,
    tr,
):
    fmin = first_value = filter_ranges[filter_dropdown.selected_key][0]
    fmax = first_value = filter_ranges[filter_dropdown.selected_key][1]

    tr_filt = tr.copy()
    tr_filt.filter("bandpass", freqmin=fmin, freqmax=fmax, corners=4, zerophase=True)
    tr_filt.data = tr_filt.data / max(abs(tr_filt.data))
    t = tr_filt.times("relative")

    arrivals = model.get_travel_times(
        source_depth_in_km=event_depth_km,
        distance_in_degree=distance_deg,
        phase_list=phase_types
    )
    color = random.choice(colors)

    fig = plt.figure(figsize=(15, 6))
    plt.plot(t, tr_filt.data, label=f'{fmin}–{fmax} Hz', color=color)
    plt.xlabel("Time after(s)")
    plt.ylabel("Amplitude")
    plt.title(f"{selected_network}.{selected_station}.{selected_channel} | {selected_event} | {fmin}-{fmax} Hz")

    for arr in arrivals:
        if arr.name in arrival_colors:
            plt.axvline(arr.time, color=arrival_colors[arr.name], linestyle='--', label=arr.name)

    plt.grid(True)
    plt.tight_layout()

    fig
    return (tr_filt,)


@app.cell
def _(np, plt, spectrogram, tr_filt):
    sampling_rate = tr_filt.stats.sampling_rate
    sampling_rate = 66150

    fig2 = plt.figure(figsize=(10, 4))
    frequencies, time_segments, Sxx = spectrogram(tr_filt.data, fs=sampling_rate, nperseg=1024, noverlap=256, scaling='spectrum')
    plt.pcolormesh(time_segments, frequencies, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis', vmin=-99)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.title('Original Signal Spectrogram')
    plt.colorbar(label='Intensity [dB]')
    plt.ylim(0, 1000)
    fig2
    return


@app.cell
def _(event_lat, event_lon, station_info, station_lat, station_lon):
    fig5 = generate_rose_plot(event_lat, event_lon, station_lat, station_lon, station_info)
    return (fig5,)


@app.cell
def _(fig5):
    fig5
    return


@app.cell(column=4)
def _(mo):
    mo.md(r"""## HYDROPHONES""")
    return


@app.cell
def _(mo):
    mo.md(r"""This section isn't quite ready yet. Come back later to see how ecologists can use hydrophones to understand biological populations.""")
    return


@app.cell(column=5)
def _(basePath, mo):
    mo.image(
        src=  basePath / "Images" / "logo.png",
        alt="Logo",
        width=100,
        height=100,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Thanks for your RiptideRemix! Your journey through sound has brought together whispers, rumbles, and songs of the sea. We’re so glad you set sail with us. Now take your creation, share it, and let it ripple out into the world.""")
    return


@app.cell
def _(mo):
    mo.md(r"""Derya""")
    return


@app.cell
def _(mo):
    mo.md(r"""Mattie""")
    return


@app.cell
def _(mo):
    mo.md(r"""Isabelle""")
    return


@app.cell
def _(mo):
    mo.md(r"""Kasey""")
    return


@app.cell
def _(mo):
    mo.md(r"""Oluwatofunmi""")
    return


@app.cell
def _(mo):
    mo.md(r"""Dwight""")
    return


@app.cell(column=6)
def _(mo):
    mo.md(r"""# Underlying Python functions""")
    return


@app.cell
def _(ccrs, cfeature, plt):
    def plot_event_station_map(event_lat, event_lon, station_lat, station_lon, station_info):
        fig = plt.figure(figsize=(10, 5))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_title(f"Map: {station_info['network']}.{station_info['station']} and Earthquake", fontsize=14)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAKES, alpha=0.5)
        ax.add_feature(cfeature.RIVERS)
        ax.plot(station_lon, station_lat, marker='^', markersize=12, color='gold', label='Station')
        ax.plot(event_lon, event_lat, marker='*', markersize=16, color='red', label='Earthquake')
        ax.plot([station_lon, event_lon], [station_lat, event_lat], color='gray', linestyle='--', linewidth=1)
        ax.text(station_lon + 1, station_lat + 1, station_info['station'], fontsize=9, color='black')
        ax.text(event_lon + 1, event_lat + 1, "EQ", fontsize=9, color='darkred')
        lat_min = min(event_lat, station_lat) - 60
        lat_max = max(event_lat, station_lat) + 60
        lon_min = min(event_lon, station_lon) - 40
        lon_max = max(event_lon, station_lon) + 40
        ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        ax.gridlines(draw_labels=True, linestyle='--')
        ax.legend(loc='upper right', fontsize=10)
        plt.tight_layout()
        return fig
    return (plot_event_station_map,)


@app.function
def generate_rose_plot(event_lat, event_lon, station_lat, station_lon, station_info):
    from obspy.geodetics import gps2dist_azimuth
    import matplotlib.pyplot as plt
    import numpy as np

    _, azimuth, back_azimuth = gps2dist_azimuth(event_lat, event_lon, station_lat, station_lon)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(7, 6))
    ax.set_theta_zero_location('N')    # North at the top
    ax.set_theta_direction(-1)         # Clockwise
    ax.set_title(f"Azimuth from EQ to {station_info['station']}", va='bottom', fontsize=14)
    ax.bar(np.deg2rad(azimuth), 1, width=np.deg2rad(4), color='red', alpha=0.3, label='Azimuth (EQ ➝ Station)')
    ax.bar(np.deg2rad(back_azimuth), 1, width=np.deg2rad(4), color='blue', alpha=0.3, label='Back-Azimuth')
    ax.plot(np.deg2rad(azimuth), 1.05, marker='*', markersize=15, color='red', label='Earthquake')
    ax.plot(np.deg2rad(back_azimuth), 1.05, marker='^', markersize=10, color='gold', label='Station')
    ax.set_yticklabels([])
    ax.set_rmax(1.2)
    ax.text(0, 1.15, 'N', ha='center', va='center', fontsize=12)
    ax.text(np.pi/2, 1.15, 'E', ha='center', va='center', fontsize=12)
    ax.text(np.pi, 1.15, 'S', ha='center', va='center', fontsize=12)
    ax.text(3*np.pi/2, 1.15, 'W', ha='center', va='center', fontsize=12)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    app.run()
