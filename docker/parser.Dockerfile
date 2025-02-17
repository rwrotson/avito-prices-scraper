# Based on:
# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile

# STAGE 1: Build the application
ARG BASE_IMAGE_TAG=3.13.1-bookworm

FROM python:${BASE_IMAGE_TAG} AS builder

# To optimize the build, set the following environment variables, due to:
# https://docs.astral.sh/uv/guides/integration/docker/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install dependencies for Chrome webdriver
RUN apt update && apt install -y libnss3 libnspr4

# Install Chrome browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv by copying the binary from the official distroless Docker image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install the project's dependencies using the lockfile and settings
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Add the rest of the project source code and install it (Installing separately from its dependencies allows optimal layer caching)
COPY ../src README.md LICENSE /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# STAGE 2: Run the application
# It is important to use the image that matches the builder, as the path to the Python executable must be the same
ARG BASE_IMAGE_TAG=3.13.1-bookworm

FROM python:${BASE_IMAGE_TAG} AS runner

# Copy Chrome and its dependencies from builder
COPY --from=builder /usr /usr
COPY --from=builder /etc /etc
COPY --from=builder /opt /opt

# Create a non-root user for security
RUN groupadd --system appgroup && useradd --system --create-home --gid appgroup appuser

# Copy the application from the builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Place executables in the environment at the front of the path and set other environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DISPLAY=:99 \
    COLUMNS=200 \
    FORCE_COLOR=1 \
    CHROME_BINARY="/usr/bin/google-chrome"

WORKDIR /app

# Switch to the non-root user
USER appuser

# Mount the logs directory as a volume
VOLUME /app/logs
VOLUME /app/media

# Run the application by default
CMD ["python", "-m", "main", "search-on-avito-from-file", "./request_entries/example.yaml", "--max-pages", "5", "--min-price", "20"]
