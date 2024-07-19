# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR .
# Install dependencies

COPY requirements.txt .
RUN pip install -r /requirements.txt

# Copy the current directory contents into the container at /app
COPY . .



# Expose port 5000 (Flask default)
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]