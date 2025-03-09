# DuraCloud Content Retrieval Tool

A modern web interface for downloading content from DuraCloud storage spaces. This tool replaces the traditional command-line interface with a user-friendly web application that works across all platforms.

**Author:** Krishna Pareek  

## ✨ Features

- 🌐 Modern web interface with real-time progress tracking
- 📦 Batch download support via content list files
- 🔒 Secure credential handling
- 📁 Cross-platform file management
- 🐳 Docker containerization for easy deployment
- ⚙️ Flexible configuration via environment variables

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- PowerShell (Windows) or Terminal (macOS/Linux)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kgitbit/duracloud-retrieval-web.git
   cd duracloud-retrieval-web
   ```

2. Configure environment:
   ```bash
   cp app/.env.template app/.env
   ```

   **Required Configuration:**
   You MUST configure the `HOST` variable in your `.env` file to match your institution's DuraCloud host:
   ```bash
   # Example .env configuration
   HOST=your-institution.duracloud.org    # Replace with your institution's host
   ```

   This configuration is required for the application to connect to your institution's DuraCloud instance.
   Do not use any default values - the host must be specifically configured for your institution.

3. Start the application:
   ```bash
   cd app/docker
   docker compose up --build -d
   ```

4. Access the web interface at `http://localhost:5000`

## 📂 Project Structure

```
duracloud-retrieval-web/
├── app/
│   ├── docker/             # Docker configuration
│   │   ├── Dockerfile     # Container definition
│   │   └── docker-compose.yml
│   ├── frontend/          # Web interface
│   │   └── index.html    # Main interface
│   ├── server.py          # Flask server
│   └── requirements.txt   # Python dependencies
├── downloads/            # Downloaded files
├── duracloud-logs/       # Application logs
└── content/             # Content list files
```

## 🔧 Usage

1. Open `http://localhost:5000` in your browser
2. Enter your DuraCloud credentials
3. Select your space and upload a content list file
4. Choose download directory
5. Start the download process
6. Monitor progress in real-time

## 🛠️ Docker Commands

### Windows (PowerShell)
```powershell
.\docker-commands.ps1 <command>
```
Available commands:
- `rebuild` - Rebuild and start containers
- `restart` - Restart containers
- `logs` - View container logs
- `clean` - Remove containers
- `status` - Check container status

### macOS/Linux
```bash
docker compose -f app/docker/docker-compose.yml <command>
```
Common commands:
- `up --build` - Build and start containers
- `down` - Stop containers
- `logs` - View logs
- `ps` - Check status

## 🔍 Troubleshooting

### Common Issues

1. Port Conflicts
   ```
   Error: Port 5000 already in use
   Solution: Change port in docker-compose.yml or stop conflicting service
   ```

2. Permission Issues
   ```
   Error: Permission denied for downloads directory
   Solution: Check directory permissions and ownership
   ```

3. Connection Problems
   ```
   Error: Unable to connect to DuraCloud
   Solution: Verify credentials and network connectivity
   ```

For more detailed troubleshooting, see [DOCUMENTATION.md](DOCUMENTATION.md)

## 📚 Documentation

- [Technical Documentation](DOCUMENTATION.md) - Detailed technical guide
- [DuraCloud Wiki](https://wiki.lyrasis.org/display/DURACLOUDDOC/DuraCloud+Retrieval+Tool) - Official DuraCloud documentation

## 🤝 Support

- Technical issues: [krishna.opensource.dev@gmail.com](mailto:krishna.opensource.dev@gmail.com)
- DuraCloud service: Contact your institution's DuraCloud administrator

## 📄 License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

### Attribution

This work is a derivative of DuraCloud, Copyright 2009-2019 DuraSpace. 