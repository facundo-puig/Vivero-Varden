FROM python:3.12-slim

# uv, copiado desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Primero solo las dependencias, para aprovechar la caché de Docker
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .

EXPOSE 8000

# Valor por defecto (producción). En desarrollo, compose lo reemplaza.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]