from typing import Annotated, Callable, Coroutine
from fastapi.responses import HTMLResponse, RedirectResponse
import marimo
from fastapi import FastAPI, Form, Request, Response
import platform
from pathlib import Path

# Detect OS and set project root accordingly
if platform.system() == "Windows":
    basePath = Path("C:/Users/kasey/Desktop/ohw25_proj_RiptideRemix")
else:
    basePath = Path("/home/jovyan/ohw25_proj_RiptideRemix")


# Create a marimo asgi app
server = (
    marimo.create_asgi_app()
    .with_app(path="", root= basePath / "contributor_folders" / "kasey" / "mixer_page.py")
    .with_app(path="/about", root= basePath / "contributor_folders" / "kasey" / "about_team.py")
    .with_app(path="/learn", root = basePath / "contributor_folders" / "kasey" / "learn_more.py")
    .with_app(path="/quake", root = basePath / "contributor_folders" / "kasey" / "visualize_quakes.py")
)

# Create a FastAPI app
app = FastAPI()
app.mount("/", server.build())


host_ip = "10.19.147.127"

# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=host_ip, port=8000)
