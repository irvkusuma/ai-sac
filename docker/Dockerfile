
FROM python:3.12-slim-bookworm

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /workspace

# Python environment configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_LINK_MODE=copy
ENV PATH="/opt/venv/bin:$PATH"

# Install project dependencies
#COPY pyproject.toml README.md ./

#RUN uv sync --no-install-project

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-install-project

# Create workspace
RUN mkdir -p /workspace/notebooks

EXPOSE 8888

CMD ["sh", "-c", \
     "uv run --no-sync jupyter lab \
     --ip=0.0.0.0 \
     --port=8888 \
     --no-browser \
     --ServerApp.root_dir=/workspace \
     --ServerApp.token=\"$JUPYTER_TOKEN\""]
