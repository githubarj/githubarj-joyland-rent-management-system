
# STAGE 1: Base

FROM python:3.10-alpine3.22 AS base


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_CACHE_DIR=/tmp/pip-cache

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# STAGE 2: Development

FROM base AS development

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# STAGE 3: Production

FROM base AS production

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . .

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN chown -R django:django /app

USER django

EXPOSE 8000

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "config.wsgi:application"]