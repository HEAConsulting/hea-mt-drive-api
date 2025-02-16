# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Command to run the API with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "google_drive_api_server:app"]
