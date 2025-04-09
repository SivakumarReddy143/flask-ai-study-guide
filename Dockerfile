# Use a pinned slim-buster image for better compatibility
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Command to run your app
CMD ["python", "run.py"]
