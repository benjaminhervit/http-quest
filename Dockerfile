# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Prevent Python from writing .pyc files and force stdout flushing
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Only copy the requirements first to leverage Docker layer caching
COPY requirements.txt /app/

# Install runtime deps
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Now copy the actual app code
COPY . /app

# If you use a .env file, Flask can read it if python-dotenv is installed (you have it)
# Set your module here if needed, e.g. "httpquest.app" or "app"
ENV FLASK_APP=httpquest:app
# Or if you use an app factory:
# ENV FLASK_APP=httpquest:create_app

EXPOSE 8000

# Start the dev server (simple & plug-n-play).
# For production, prefer the gunicorn example below.
ENV FLASK_APP=wsgi:app
CMD ["python","-m","flask","run","--host=0.0.0.0","--port=8000"]
