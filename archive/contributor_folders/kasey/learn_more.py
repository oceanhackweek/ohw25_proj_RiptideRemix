import marimo

__generated_with = "0.14.17"
app = marimo.App(
    width="columns",
    app_title="RiptideRemix_mixer",
    layout_file="layouts/learn_more.grid.json",
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
        src= basePath / "Images" / "LearnMore" / "eq.jpeg",
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
        src= basePath / "Images" / "LearnMore" / "bowhead.jpeg",
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
        src= basePath / "Images" / "LearnMore" / "humpback.jpeg",
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
        src= basePath / "Images" / "LearnMore" / "ib.jpg",
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
        src= basePath / "Images" / "LearnMore" / "orca.jpeg",
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
        src= basePath / "Images" / "LearnMore" / "sperm.jpeg",
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
    ## Earthquakes
    Underwater earthquakes send out deep, booming rumbles that can travel thousands of miles through the ocean. Acoustic researchers “listen” to these sounds to track seismic activity, map tectonic plates, and even study how energy moves through the Earth.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Bowhead Whale
    Bowhead whales, living in icy Arctic waters, create an incredible variety of songs—sometimes switching “tunes” from year to year. Acoustic monitoring helps researchers follow their movements beneath the ice, study their cultural song traditions, and understand how climate change impacts their habitat.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Orcas
    Orcas are masters of sound, using clicks, whistles, and calls to hunt and communicate. Researchers track these acoustic “dialects” to study pod culture, migration paths, and the intricate relationships within orca families.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Icebergs
    Icebergs crack, groan, and fizz as they break apart and melt, creating a symphony of icy sounds. Scientists use these acoustic clues to monitor iceberg movement, track melting rates, and better understand how climate change is reshaping our polar seas.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Sperm Whale
    Sperm whales communicate using patterns of clicks called codas, forming distinct dialects for different family groups. Acoustic recordings allow scientists to decode these social structures, follow deep-diving hunts, and reveal how whale cultures pass knowledge across generations.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Humpback Whale
    Humpbacks sing long, complex songs that can travel across entire ocean basins. By recording and analyzing these melodies, researchers learn how whales communicate, track migration routes, and even study how ocean noise affects marine life.
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
    nav_menu = mo.nav_menu({
        "/": "Mix Sounds",  # internal
        "/learn": "Learn More",  # internal
        "/about": "About the Team",  # internal
        "/quake": "Gather More Data"
    })
    nav_menu
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
