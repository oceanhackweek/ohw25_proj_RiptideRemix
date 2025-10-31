import marimo

__generated_with = "0.14.17"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Riptide Remix

    The goal of this project is to create a web interface where users can combine marine soundscape audio clips (e.g. whale calls, earthquakes, ships) to create music. Think GarageBand, but with marine science!

    Right now, this notebook is just for testing out various interactive elements unique to Marimo.
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    return


@app.cell
def _(mo):
    checkbox = mo.ui.checkbox(label="Loop audio")
    return (checkbox,)


@app.cell
def _(mo):
    mo.image(
        src="/home/jovyan/ohw25_proj_RiptideRemix/Images/ArtGifs/placeholder.gif",
        alt="placeholder",
        width=750,
        height=200,
        rounded=False,
        caption=""
    )
    return


@app.cell
def _(checkbox, mo):
    mo.hstack([checkbox, mo.md(f"Has value: {checkbox.value}")])
    return


@app.cell
def _(checkbox):
    if checkbox.value:
        print('check!')
    return


@app.cell
def _(mo):
    increment_button = mo.ui.button(
        value=0, on_click=lambda value: value + 1, label="increment", kind="warn"
    )
    return (increment_button,)


@app.cell
def _(increment_button):
    increment_button.value
    return


@app.cell
def _(increment_button):
    increment_button
    return


@app.cell
def _(mo):
    # a button that when clicked will have its value set to True;
    # any cells referencing that button will automatically run.
    button = mo.ui.run_button()
    button
    return (button,)


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 10)
    slider
    return (slider,)


@app.cell
def _(mo):
    slider_auto = mo.ui.slider(1, 10, label='Frequency? Hertz?')
    slider_auto
    return


@app.cell
def _(button, mo, slider):
    # if the button hasn't been clicked, don't run.
    mo.stop(not button.value)

    slider.value
    return


@app.cell
def _(mo):
    dropdown = mo.ui.dropdown(options={'Seismic activity': 1, 'Whale song': 2}, value='Seismic activity')
    return (dropdown,)


@app.cell
def _(dropdown):
    dropdown
    return


@app.cell
def _(dropdown):
    if dropdown.selected_key == 'Seismic activity':
        display = 'seismic event recordings'
    elif dropdown.selected_key == 'Whale song':
        display = 'whale song recordings'
    else:
        display = 'ERROR'

    print(f'Currently displaying {display}')
    return


@app.cell
def _(mo):
    mo.md(r"""What if users had the option to save their song when they were happy with it?""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
