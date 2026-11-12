
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

## Development

Start environment:

```bash
docker compose up -d --build
```

Stop environment:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f app
```

Access JupyterLab:

http://localhost:8888

## Project Structure

- docker/: Docker configuration
- notebooks/: Jupyter notebooks
- src/: Application source code
- data/: Data storage
- tests/: Unit tests
- docs/: Technical documentation
