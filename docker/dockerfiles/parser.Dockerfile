# Based on:
# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile

# STAGE 1: Build the application
ARG BASE_IMAGE_TAG=3.13.1-bookworm

FROM python:${BASE_IMAGE_TAG} AS builder

# To optimize the build, set the following environment variables, due to:
# https://docs.astral.sh/uv/guides/integration/docker/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install Chrome browser
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt update && apt install -y \
      libnss3 \
      libnspr4 \
      ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv by copying the binary from the official distroless Docker image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG PROJECT_EDITION=minimal

WORKDIR /app

# Install the project's dependencies using the lockfile and settings
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$PROJECT_EDITION" = "full" ]; then \
        uv sync --frozen --no-install-project --no-dev --extra db-libs; \
    else \
        uv sync --frozen --no-install-project --no-dev; \
    fi

# Add the rest of the project source code and install it (Installing separately from its dependencies allows optimal layer caching)
COPY ../../src README.md LICENSE ./
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

ARG USER=appuser
ARG GROUP=appgroup

# Create a non-root user for security
RUN groupadd --system ${GROUP} && \
    useradd --system --create-home --gid ${GROUP} ${USER}

ARG HOME="/home/$USER/src"
WORKDIR $HOME

# Copy the application from the builder
COPY --from=builder --chown=${USER}:${GROUP} /app $HOME

# Place executables in the environment at the front of the path and set other environment variables
ENV PATH="$HOME/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DISPLAY=:99 \
    COLUMNS=200 \
    FORCE_COLOR=1 \
    CHROME_BINARY="/usr/bin/google-chrome"

# Switch to the non-root user
USER $USER
