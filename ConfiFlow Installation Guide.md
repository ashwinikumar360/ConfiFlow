# ConfiFlow Installation Guide

**Author**: Ashwini Kumar Tarai  
**Last Updated**: June 26, 2025

This comprehensive installation guide will walk you through setting up ConfiFlow on your local machine or server. ConfiFlow is designed to be completely self-hosted, giving you full control over your data and processing capabilities.

## System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10/11
- **RAM**: 8GB (16GB recommended for AI processing)
- **Storage**: 20GB free space (additional space needed for AI models)
- **CPU**: Multi-core processor (GPU recommended for AI workloads)
- **Network**: Internet connection for initial setup and package downloads

### Recommended Requirements
- **RAM**: 32GB or more for large language models
- **GPU**: NVIDIA GPU with 8GB+ VRAM for optimal AI performance
- **Storage**: SSD with 100GB+ free space
- **CPU**: Modern multi-core processor (Intel i7/AMD Ryzen 7 or better)

## Prerequisites Installation

### Ubuntu/Debian Systems

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential curl wget git

# Install Node.js and pnpm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g pnpm

# Install Python and pip
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install system dependencies for document processing
sudo apt install -y poppler-utils pandoc tesseract-ocr festival

# Install additional OCR language packs (optional)
sudo apt install -y tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-deu

# Install multimedia processing tools
sudo apt install -y ffmpeg imagemagick

# Install database tools (optional, for PostgreSQL support)
sudo apt install -y postgresql postgresql-contrib libpq-dev
```

### macOS Systems

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js and pnpm
brew install node
npm install -g pnpm

# Install Python
brew install python@3.11

# Install system dependencies
brew install poppler pandoc tesseract festival

# Install multimedia tools
brew install ffmpeg imagemagick

# Install database tools (optional)
brew install postgresql
```

### Windows Systems

For Windows, we recommend using Windows Subsystem for Linux (WSL2) for the best experience:

```powershell
# Enable WSL2 (run as Administrator)
wsl --install

# After reboot, install Ubuntu from Microsoft Store
# Then follow the Ubuntu installation instructions above
```

Alternatively, you can install dependencies directly on Windows:

1. Install Node.js from [nodejs.org](https://nodejs.org)
2. Install Python from [python.org](https://python.org)
3. Install Git from [git-scm.com](https://git-scm.com)
4. Install additional tools manually or use package managers like Chocolatey

## AI Services Installation

### Ollama (Local Language Models)

Ollama provides an easy way to run large language models locally:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull recommended models
ollama pull llama3
ollama pull mistral
ollama pull codellama

# Verify installation
ollama list
```

### Whisper (Speech Recognition)

```bash
# Install Whisper via pip
pip3 install openai-whisper

# Download models (optional, will download automatically on first use)
whisper --model base --help
```

### N8N (Workflow Automation)

```bash
# Install N8N globally
npm install -g n8n

# Create N8N data directory
mkdir -p ~/.n8n

# Start N8N (will create initial configuration)
n8n start &

# Access N8N at http://localhost:5678
```

## ConfiFlow Installation

### 1. Clone the Repository

```bash
# Clone the main repository
git clone https://github.com/ashwinikumartarai/confiflow.git
cd confiflow

# Verify directory structure
ls -la
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd confiflow-ui

# Install dependencies
pnpm install

# Verify installation
pnpm run build

# Start development server (optional)
pnpm run dev
```

The frontend will be available at `http://localhost:5173` in development mode.

### 3. Backend Setup

```bash
# Navigate to backend directory
cd ../confiflow-backend

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"

# Start backend server
python src/main.py
```

The backend API will be available at `http://localhost:5000`.

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
cd confiflow-backend
cat > .env << EOF
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# AI Service URLs
OLLAMA_URL=http://localhost:11434/api/generate
N8N_URL=http://localhost:5678
N8N_API_KEY=

# Database Configuration
DATABASE_URL=sqlite:///app.db

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads

# Security Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
EOF
```

### N8N Configuration

1. Access N8N at `http://localhost:5678`
2. Complete the initial setup wizard
3. Create an API key in Settings > API Keys
4. Update the `N8N_API_KEY` in your `.env` file

### Ollama Model Configuration

```bash
# List available models
ollama list

# Pull additional models as needed
ollama pull phi3
ollama pull gemma

# Test model functionality
ollama run llama3 "Hello, how are you?"
```

## Verification and Testing

### 1. Frontend Testing

```bash
cd confiflow-ui

# Run tests
pnpm test

# Build for production
pnpm run build

# Preview production build
pnpm run preview
```

### 2. Backend Testing

```bash
cd confiflow-backend
source venv/bin/activate

# Test API endpoints
curl http://localhost:5000/api/health

# Test AI integration
curl -X POST http://localhost:5000/api/ai/ollama/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!", "model": "llama3"}'
```

### 3. Integration Testing

```bash
# Test document upload and processing
curl -X POST http://localhost:5000/api/ai/document/extract \
  -F "document=@sample.pdf"

# Test N8N webhook
curl -X POST http://localhost:5000/api/n8n/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## Production Deployment

### Docker Deployment

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  frontend:
    build: ./confiflow-ui
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./confiflow-backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/confiflow
    depends_on:
      - db
      - ollama

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=confiflow
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  ollama_data:
  n8n_data:
```

Deploy with Docker Compose:

```bash
docker-compose up -d
```

### Traditional Server Deployment

For traditional server deployment:

1. **Setup reverse proxy** (Nginx/Apache)
2. **Configure SSL certificates** (Let's Encrypt)
3. **Setup process management** (systemd/supervisor)
4. **Configure monitoring** (logs, metrics)
5. **Setup backup procedures** (database, files)

## Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check which process is using a port
sudo lsof -i :5000
sudo lsof -i :5173

# Kill process if needed
sudo kill -9 <PID>
```

#### Permission Issues
```bash
# Fix Python virtual environment permissions
sudo chown -R $USER:$USER confiflow-backend/venv

# Fix Node.js permissions
sudo chown -R $USER:$USER ~/.npm
```

#### AI Service Connection Issues
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Check N8N status
curl http://localhost:5678/healthz

# Restart services if needed
pkill ollama && ollama serve &
pkill n8n && n8n start &
```

### Log Files

Monitor application logs for debugging:

```bash
# Backend logs
tail -f confiflow-backend/logs/app.log

# Frontend build logs
cd confiflow-ui && pnpm run build --verbose

# System service logs
journalctl -u ollama -f
journalctl -u n8n -f
```

## Performance Optimization

### System Optimization

```bash
# Increase file descriptor limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize Python performance
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1

# Configure swap for memory management
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Database Optimization

For PostgreSQL production deployments:

```sql
-- Optimize PostgreSQL settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
SELECT pg_reload_conf();
```

## Security Considerations

### Basic Security Setup

```bash
# Setup firewall
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Secure file permissions
chmod 600 confiflow-backend/.env
chmod -R 755 confiflow-ui/dist
```

### SSL/TLS Configuration

For production deployments, configure SSL certificates:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com
```

## Maintenance

### Regular Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Node.js dependencies
cd confiflow-ui && pnpm update

# Update Python dependencies
cd confiflow-backend && source venv/bin/activate && pip install -U -r requirements.txt

# Update AI models
ollama pull llama3
```

### Backup Procedures

```bash
# Backup database
pg_dump confiflow > backup_$(date +%Y%m%d).sql

# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz confiflow-backend/.env confiflow-ui/.env*

# Backup user data
rsync -av uploads/ backup/uploads/
```

---

**Author**: Ashwini Kumar Tarai  
**Support**: For installation issues, please create an issue on GitHub or refer to the troubleshooting section above.

