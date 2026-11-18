
# AI SAC

AI-powered analytics platform for SAP Analytics Cloud.

## Architecture

- Python 3.12
- Pandas / NumPy
- JupyterLab
- uv
- Docker
- DuckDB (Phase 4)
- AI Layer (Phase 5)

## Restore and run with Docker

### After reinstalling the operating system

Clone the repository and enter the project directory:

```bash
git clone https://github.com/irvkusuma/ai-sac.git "$HOME/Projects/ai-sac"
cd "$HOME/Projects/ai-sac"
```

Restore `.env` from its encrypted local backup. Replace the example path with the actual location of that backup. The `.env` file contains credentials and is intentionally not stored in GitHub.

```bash
gpg --decrypt /path/to/ai-sac.env.gpg > .env
chmod 600 .env
```

Once the project data artifacts are committed to GitHub, cloning the repository restores them under `data/`. Install and start Docker Engine with the Compose plugin, then build and start the app:

```bash
docker compose up -d --build
```

Check the container and follow its logs:

```bash
docker compose ps
docker compose logs -f app
```

Open JupyterLab at <http://localhost:8888>. Use the token configured in the restored `.env` file.

### Start and stop

Start containers that were stopped with `docker compose stop`:

```bash
docker compose start
```

Stop the app while keeping its container and named volume:

```bash
docker compose stop
```

Remove the containers and Compose network while keeping the named volume:

```bash
docker compose down
```

`docker compose down -v` also deletes the named `ai-sac-venv` volume. Use it only when you intend to remove that environment volume. The volume can be rebuilt from the Dockerfile and `uv.lock`.

### Rebuild after changing dependencies

```bash
docker compose up -d --build
```

## Project Structure

- docker/: Docker configuration
- notebooks/: Jupyter notebooks
- src/: Application source code
- data/: Data storage
- tests/: Unit tests
- docs/: Technical documentation
