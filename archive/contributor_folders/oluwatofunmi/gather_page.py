import marimo

__generated_with = "0.14.17"
app = marimo.App(
    width="columns",
    app_title="RiptideRemix_mixer",
    layout_file="layouts/about_team.grid.json",
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


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "Folks" / "kasey.jpg",
        alt="placeholder",
        width=175,
        height=200,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "Folks" / "mattie.jpg",
        alt="placeholder",
        width=175,
        height=200,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "Folks" / "dwight.jpg",
        alt="placeholder",
        width=175,
        height=200,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "Folks" / "derya.jpg",
        alt="placeholder",
        width=200,
        height=200,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "Folks" / "isabelle.jpg",
        alt="placeholder",
        width=175,
        height=200,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "Folks" / "oluwatofunmi.jpeg",
        alt="placeholder",
        width=175,
        height=200,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Kasey Castello

    Kasey is a first-year student at Scripps Institution of Oceanography studying Bioacoustics under the supervision of Kait Frasier. Her favorite marine sound is a baby crocodile contact call.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Mattie Toll

    Mattie is a researcher at Ocean Science Analytics working on bioacoustics programming. Her favorite marine sound is a dwarf-minke whale.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Isabelle Brandicourt

    Isabelle is a first-year PhD student at the University of Washington studying distributed acoustic sensing under the supervision of Shima Abadi. Her favorite oceanic sound is ORCA-JPOD-S10.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Derya Gumustel

    Derya is web-developer at Sound Data Science. Her favorite oceanic sound is an osprey call.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Oluwatofunmi Adeboye

    Oluwatofunmi is a second-year MS student at the University of Hawaii at Manoa studying Geophysics. His favorite oceanic sound is an earthquake.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Dwight Owens

    Dwight is a Development Manager at Ocean Networks Canada and served as a mentor for this project. His favorite oceanic sound is a fish grunt.
    """
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
    import webbrowser
    gather_button = mo.ui.button(
        label="Gather Data",
        kind='neutral',
        on_click=lambda _: webbrowser.open("http://10.19.147.127:8000/gather", new=0)  # URL for Gather page
    )
    gather_button
    return (webbrowser,)


@app.cell
def _(mo, webbrowser):
    mix_button = mo.ui.button(
        label="Mix Sounds",
        kind='neutral',
        on_click=lambda _: webbrowser.open("http://10.19.147.127:8000/", new=0)  # URL for Mixer page
    )
    mix_button
    return


@app.cell
def _(mo, webbrowser):
    educate_button = mo.ui.button(
        label="Learn More",
        kind='neutral',
        on_click=lambda _: webbrowser.open("http://10.19.147.127:8000/learn", new=0)  # URL for Learn More
    )
    educate_button
    return


@app.cell
def _(mo, webbrowser):
    about_button = mo.ui.button(
        label="About the Team",
        kind='neutral',
        on_click=lambda _: webbrowser.open("http://10.19.147.127:8000/about", new=0)  # URL for About
    )
    about_button
    return


@app.cell(column=2)
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


if __name__ == "__main__":
    app.run()
