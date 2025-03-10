FROM python:3.11-slim

# Install OpenJDK-17
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/frontend/ frontend/
COPY app/server.py .
COPY retrievaltool-8.0.0-driver.jar .

# Create necessary directories
RUN mkdir -p downloads content duracloud-logs

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=production
ENV PORT=5000

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]