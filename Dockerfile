FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock first (for caching)
COPY Pipfile Pipfile.lock* ./

# Install dependencies system-wide (so Django runs normally)
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system

# Copy the rest of the app
COPY . .

WORKDIR /app/inventory

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]