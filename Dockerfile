# Use the official Python 3.12 image as base
FROM python:3.12-slim

# Install build dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run Django server
CMD ["python", "backend_api/manage.py", "runserver", "0.0.0.0:8000"]
