FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env  # ✅ This line copies the .env file into the image

CMD ["python", "run.py"]
