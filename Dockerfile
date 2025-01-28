FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend .

# Expose API port
EXPOSE 8000

# Create volume for ChromaDB persistence
VOLUME /app/vector_store

# Start FastAPI app
CMD ["python", "-m", "app.main"]