# STAGE 1: Base
FROM python:3.10-alpine AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_CACHE_DIR=/tmp/pip-cache
WORKDIR /app
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    curl

# STAGE 2: Development
FROM base AS development
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# STAGE 3: Production
FROM base AS production
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
RUN addgroup -S django \
    && adduser -S -G django django
RUN mkdir -p /app/staticfiles \
    && chown -R django:django /app
USER django
EXPOSE 8000
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "server_joyland.wsgi:application"]
