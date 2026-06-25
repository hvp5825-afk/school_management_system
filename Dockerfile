FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn whitenoise

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "school_management.wsgi:application"]
