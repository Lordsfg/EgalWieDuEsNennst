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

# Copy wait-for-it.sh script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh

# Set execute permissions for the script
RUN chmod +x /app/wait-for-it.sh

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run Django server with wait-for-it.sh script
CMD ["sh", "-c", "/app/wait-for-it.sh db:3306 -- python backend_api/manage.py runserver 0.0.0.0:8000"]
