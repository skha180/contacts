# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
<<<<<<< HEAD
    libpq-dev \
=======
>>>>>>> 23894a8 (Update settings.py for static files and update Dockerfile for Render deployment)
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

<<<<<<< HEAD
# Set Django environment variables (can be overridden in Render)
ENV DJANGO_SETTINGS_MODULE=contacts.settings
ENV PORT 8000
ENV DEBUG=0

=======
>>>>>>> 23894a8 (Update settings.py for static files and update Dockerfile for Render deployment)
# Ensure static root exists
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "contacts.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
