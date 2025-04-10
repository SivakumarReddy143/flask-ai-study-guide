# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim-buster

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the contents of the current directory into /app in the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 5000 (default Flask port) for accessing the app externally
EXPOSE 5000

# Set the default command to run your Flask app
CMD ["python3", "app.py"]
