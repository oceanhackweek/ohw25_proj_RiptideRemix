# syntax=docker/dockerfile:1.17
FROM ghcr.io/prefix-dev/pixi:0.52.0-noble@sha256:48b6892ecfd5378beb78a4b234ea46343bf14ec4a790f6f2c41f5d5b9023741b

WORKDIR /app

COPY --link pixi.lock pixi.toml ./

RUN --mount=type=cache,id=riptide_remix,target=/root/.cache/rattler/cache \
    pixi install --frozen -e default

COPY --link *.py ./
COPY --link contributor_folders/kasey ./contributor_folders/kasey
COPY --link ./Images/ /home/jovyan/ohw25_proj_RiptideRemix/Images/
COPY --link ./Library/ /home/jovyan/ohw25_proj_RiptideRemix/Library/

RUN mkdir __marimo__ && \
    chmod -R 777 __marimo__

EXPOSE 10000

RUN useradd -m app_user
USER app_user

ENV MARIMO_SKIP_UPDATE_CHECK=1

CMD ["pixi", "run", "--frozen", "serve"]

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:10000/health || exit 1
