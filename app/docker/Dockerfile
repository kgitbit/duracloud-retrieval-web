FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Java and Python
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk python3.9 python3.9-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY app/requirements.txt .
COPY app/server.py .
COPY app/db_operations.py .
COPY app/frontend/index.html .
COPY app/retrievaltool-8.0.0-driver.jar .

# Create and activate virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3.9 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies in virtual environment
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir uploads downloads && \
    mkdir -p /root/duracloud-retrieval-work && \
    chmod 777 /root/duracloud-retrieval-work && \
    chmod 777 downloads

# Set environment variables
ENV FLASK_PORT=5000 \
    DOWNLOAD_DIR=/app/downloads \
    CONTENT_LIST_DIR=/app/content \
    LOG_DIR=/app/logs

# Expose port
EXPOSE ${FLASK_PORT}

# Start the application using the virtual environment Python
CMD ["python", "server.py"]