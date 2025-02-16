# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Cloud Run port dynamically
ENV PORT=8080
EXPOSE $PORT

# Command to run the API with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "google_drive_api_server:app"]