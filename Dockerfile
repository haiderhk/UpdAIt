FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose API port
EXPOSE 8000

# Create volume for ChromaDB persistence
VOLUME /app/chroma_db

# Start FastAPI app
# Start ingestion.py and then the FastAPI app
CMD ["sh", "-c", "python -m data_ingestion.ingestion.py && uvicorn app:app --host 0.0.0.0 --port 8000"]