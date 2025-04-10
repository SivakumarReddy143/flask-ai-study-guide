FROM python:3.11-slim-buster

WORKDIR /app

# Copy all files and folders, including app/config/serviceAccountKey.json
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
