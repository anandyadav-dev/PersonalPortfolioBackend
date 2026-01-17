# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run uvicorn server
# Host 0.0.0.0 is crucial for Docker
# Port 8000 is default, but Render might override via PORT env var. 
# We use shell form to allow variable expansion if we passed a command, 
# but exec form is safer. We'll stick to fixed port or use shell script entrypoint if needed. 
# For Render, it's best to respect the PORT environment variable.
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
