# DuraCloud Content Retrieval Tool - Technical Documentation

## 🌐 Architecture Overview

The DuraCloud Content Retrieval Tool is a web-based application that facilitates downloading content from DuraCloud storage spaces. It provides a user-friendly interface for what was previously a command-line operation, making it accessible to users across different operating systems.

### Frontend
- 🎨 HTML5/CSS3/JavaScript with Bootstrap 5.3.0
- 📱 Responsive design for all devices
- 🎯 Font Awesome 6.0.0 for icons
- 📊 Real-time progress tracking
- Form validation and user input handling
- Cross-browser compatibility

### Backend
- 🐍 Python Flask server for web services
- ☕ Java Runtime (JRE 17+) for DuraCloud driver
- 🗄️ File system operations for downloads
- 📝 Comprehensive logging system

## 🔧 Component Details

### 1. Web Interface (`app/frontend/`)
Features:
- Single-page application design
- Real-time download progress updates
- Credential input and validation
- Space selection interface
- Download directory specification
- Content list file upload
- Status monitoring dashboard

### 2. Server (`app/server.py`)
Key Endpoints:
- `/` - Main application interface
- `/download` - Content download handler
- `/config` - Environment configuration
- `/history` - Future history feature placeholder

Features:
- Asynchronous download processing
- Error handling and logging
- File system operations
- Environment variable management

### 3. DuraCloud Driver (`retrievaltool-8.0.0-driver.jar`)
Capabilities:
- Core DuraCloud interaction component
- Authentication management
- File download handling
- Progress monitoring
- Error handling and retry logic
- Content list processing

## 📁 Project Structure

```
duracloud-retrieval-web/
├── app/
│   ├── docker/             # Docker configuration files
│   │   ├── Dockerfile     # Container definition
│   │   └── docker-compose.yml
│   ├── frontend/          # Web interface files
│   │   └── index.html    # Main interface
│   ├── server.py         # Flask application
│   ├── requirements.txt  # Python dependencies
│   └── .env.template     # Environment configuration
├── downloads/            # Downloaded files location
├── duracloud-logs/       # Application logs
├── content/             # Content list files
├── README.md
└── DOCUMENTATION.md
```

## ⚙️ Configuration

### Environment Variables

#### Required Configuration
The following environment variable MUST be configured:
```bash
HOST=                    # Your institution's DuraCloud host (e.g., your-institution.duracloud.org)
```
This is a required setting that must be configured to match your institution's specific DuraCloud host.
Do not use any default or example values - this must be set to your actual institutional host.

#### Optional Configuration
```bash
# Server Configuration
FLASK_PORT=5000           # Web server port (default: 5000)
FLASK_ENV=production      # Environment mode (default: production)

# File Paths
DOWNLOAD_DIR=            # Download directory path (default: ./downloads)
CONTENT_LIST_DIR=        # Content list directory (default: ./content)
```

### Docker Configuration
```yaml
version: '3.8'
services:
  duracloud-retrieval:
    build:
      context: ../..
      dockerfile: app/docker/Dockerfile
    ports:
      - "${FLASK_PORT:-5000}:5000"
    env_file:
      - ../../app/.env
    volumes:
      - ../../duracloud-logs:/root/duracloud-retrieval-work
      - ../../downloads:/app/downloads
```

## 🔒 Security Considerations

### 1. Authentication
- Credentials never stored permanently
- Session-based authentication
- HTTPS recommended for production
- Secure credential handling

### 2. File System Security
- Restricted download directories
- Path traversal prevention
- File permission management
- Temporary file cleanup
- Secure file name handling

### 3. Error Handling
- Sanitized error messages
- Secure logging practices
- Rate limiting
- Input validation
- Path validation

## 📊 Logging System

### Log Types
1. Application Logs
   - Server operations
   - Download status
   - Error events
   - User actions
   - Performance metrics

2. Download Logs
   - Start/completion times
   - File details
   - Success/failure status
   - Error messages
   - Progress tracking

### Log Format
```
TIMESTAMP [LEVEL] [COMPONENT] Message
2024-03-20 10:15:30 [INFO] [Server] Download started: file.pdf
2024-03-20 10:15:35 [ERROR] [Driver] Connection timeout
```

## 🔧 Troubleshooting Guide

### Common Issues

1. Connection Problems
   ```
   Issue: Unable to connect to DuraCloud
   Check:
   - Network connectivity
   - DuraCloud host URL
   - Credentials
   - Firewall settings
   - Proxy configuration
   ```

2. Download Failures
   ```
   Issue: Downloads failing or incomplete
   Check:
   - Disk space
   - File permissions
   - Network stability
   - Java heap space
   - Concurrent download limits
   ```

3. Docker Issues
   ```
   Issue: Container not starting
   Check:
   - Port conflicts
   - Volume permissions
   - Environment variables
   - Docker logs
   - Resource limits
   ```

## 🚀 Performance Optimization

### 1. Download Optimization
- Concurrent downloads with configurable limits
- Chunk-based transfers
- Progress monitoring
- Automatic retries
- Network bandwidth management

### 2. Resource Management
- Memory usage monitoring
- Disk space checking
- Connection pooling
- Process monitoring

### 3. Error Recovery
- Automatic retry logic
- Partial download resume
- Connection recovery
- Queue management

## 📈 Monitoring and Maintenance

### System Health
- CPU/Memory usage
- Disk space monitoring
- Network bandwidth
- Error rate tracking

### Maintenance Tasks
1. Log Rotation
   ```bash
   # Daily log rotation
   logrotate -d /etc/logrotate.d/duracloud
   ```

2. Temporary File Cleanup
   ```bash
   # Clean files older than 7 days
   find /tmp/duracloud -type f -mtime +7 -delete
   ```

## 🔄 Update Procedures

### Application Updates
1. Stop the application
   ```bash
   cd app/docker
   docker compose down
   ```

2. Update code
   ```bash
   # If you haven't cloned the repository yet
   git clone https://github.com/kgitbit/duracloud-retrieval-web.git
   cd duracloud-retrieval-web

   # If you already have the repository
   git pull origin main
   ```

3. Rebuild and restart
   ```bash
   docker compose up --build -d
   ```

### Driver Updates
1. Download new driver version
2. Update configuration
3. Test in staging environment
4. Deploy to production
5. Verify functionality

## 📞 Support and Contact

### Technical Support
- Email: krishna.opensource.dev@gmail.com
- Documentation: [DuraCloud Retrieval Tool](https://wiki.lyrasis.org/display/DURACLOUDDOC/DuraCloud+Retrieval+Tool)

## 🔄 Version History

### Current Version: 1.0.0
- Initial release with web interface
- Docker containerization
- Real-time download progress tracking
- Basic logging system

### Planned Future Updates
- 📊 History tracking functionality
- 📊 Enhanced download progress visualization
- 🔍 Advanced search and filtering capabilities
- Enhanced error handling and recovery
- Multi-space support
- Advanced batch processing
- Improved logging and monitoring
- User preference management

## 📄 License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

This work is a derivative of DuraCloud, Copyright 2009-2019 DuraSpace. 