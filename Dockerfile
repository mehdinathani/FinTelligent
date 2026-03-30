# Use lightweight python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Hugging Face requires port 7860!
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]