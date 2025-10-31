import marimo
from fastapi import FastAPI

server = (
    marimo.create_asgi_app()
    .with_app(path="/", root="./contributor_folders/kasey/mixer_page.py")
    .with_app(path="/about", root="./contributor_folders/kasey/about_team.py")
    .with_app(path="/learn", root="./contributor_folders/kasey/learn_more.py")
    .with_app(path="/gather", root="./contributor_folders/kasey/visualize_quakes.py")
)

app = FastAPI()

app.mount("/", server.build())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10000)
