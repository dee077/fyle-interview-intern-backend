# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py

# Expose the port that the application runs on
EXPOSE 7755

# Run the command to start the Gunicorn server
CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
