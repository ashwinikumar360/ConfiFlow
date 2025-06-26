# ConfiFlow - Open Source Research & Writing Assistant

**Author**: Ashwini Kumar Tarai  
**License**: MIT  
**Version**: 1.0.0

ConfiFlow is a comprehensive, open-source research and writing assistant platform that leverages cutting-edge AI technologies and workflow automation to streamline the research, analysis, and content creation process. Built with modern web technologies and designed for complete self-hosting capabilities, ConfiFlow provides researchers, writers, and content creators with powerful tools for document processing, AI-powered analysis, and automated workflow management.

## 🌟 Features

### Frontend Dashboard
- **Modern React Interface**: Built with React 18, providing a responsive and intuitive user experience
- **Tailwind CSS Styling**: Utility-first CSS framework for rapid UI development and consistent design
- **Lucide Icons**: Beautiful, customizable icon library for enhanced visual appeal
- **Mobile-Responsive Design**: Optimized for both desktop and mobile devices
- **Real-time Updates**: Dynamic interface updates for seamless user interaction

### AI-Powered Processing
- **Local LLM Integration**: Support for Ollama and other local language models
- **Document Analysis**: Advanced text extraction from PDF, DOCX, and other document formats
- **Audio Transcription**: Automatic speech recognition using OpenAI's Whisper
- **Text-to-Speech**: Convert text to natural-sounding speech using Festival TTS
- **Multi-format Support**: Handle various file types and content formats

### Workflow Automation
- **N8N Integration**: Seamless integration with N8N for complex workflow automation
- **Custom Workflows**: Create and manage custom research and processing workflows
- **API Orchestration**: Coordinate multiple AI services and data sources
- **Real-time Monitoring**: Track workflow execution and progress in real-time

### Document Processing
- **OCR Capabilities**: Extract text from images and scanned documents using Tesseract
- **Format Conversion**: Convert between various document formats using Pandoc
- **Web Scraping**: Extract content from web pages and online resources
- **Multimedia Processing**: Handle audio, video, and image content

## 🏗️ Architecture

ConfiFlow follows a modern microservices architecture with clear separation between frontend and backend components:

```
ConfiFlow/
├── confiflow-ui/          # React Frontend Application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Utility functions
│   │   └── assets/        # Static assets
│   └── public/            # Public assets
├── confiflow-backend/     # Flask Backend API
│   ├── src/
│   │   ├── routes/        # API route definitions
│   │   ├── models/        # Database models
│   │   └── static/        # Static file serving
│   └── venv/              # Python virtual environment
└── docs/                  # Documentation files
```

## 🚀 Quick Start

### Prerequisites

Before setting up ConfiFlow, ensure you have the following installed on your system:

- **Node.js** (v18 or later) and **pnpm**
- **Python** (3.11 or later) and **pip**
- **Git** for version control
- **System Dependencies**:
  - `poppler-utils` (for PDF processing)
  - `pandoc` (for document conversion)
  - `tesseract-ocr` (for OCR functionality)
  - `festival` (for text-to-speech)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/confiflow.git
   cd confiflow
   ```

2. **Setup Frontend**
   ```bash
   cd confiflow-ui
   pnpm install
   pnpm run dev
   ```

3. **Setup Backend**
   ```bash
   cd ../confiflow-backend
   source venv/bin/activate
   pip install -r requirements.txt
   python src/main.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# AI Service Configuration
OLLAMA_URL=http://localhost:11434/api/generate
N8N_URL=http://localhost:5678
N8N_API_KEY=your_n8n_api_key_here

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Database Configuration
DATABASE_URL=sqlite:///app.db
```

### AI Services Setup

#### Ollama (Local LLM)
1. Install Ollama from [https://ollama.ai](https://ollama.ai)
2. Pull desired models: `ollama pull llama3`
3. Start Ollama service: `ollama serve`

#### N8N (Workflow Automation)
1. Install N8N: `npm install -g n8n`
2. Start N8N: `n8n start`
3. Access N8N interface at http://localhost:5678

## 📚 API Documentation

### AI Processing Endpoints

#### Text Generation
```http
POST /api/ai/ollama/generate
Content-Type: application/json

{
  "model": "llama3",
  "prompt": "Your prompt here"
}
```

#### Audio Transcription
```http
POST /api/ai/whisper/transcribe
Content-Type: multipart/form-data

audio: [audio file]
```

#### Document Text Extraction
```http
POST /api/ai/document/extract
Content-Type: multipart/form-data

document: [PDF or DOCX file]
```

### N8N Integration Endpoints

#### Trigger Workflow
```http
POST /api/n8n/webhook/{workflow_id}
Content-Type: application/json

{
  "data": "your workflow data"
}
```

#### List Workflows
```http
GET /api/n8n/workflows
X-N8N-API-KEY: your_api_key
```

## 🛠️ Development

### Frontend Development

The frontend is built with modern React patterns and includes:

- **Component-based Architecture**: Modular, reusable components
- **Custom Hooks**: Encapsulated logic for state management and side effects
- **Tailwind CSS**: Utility-first styling approach
- **TypeScript Support**: Type-safe development (optional)

### Backend Development

The backend follows Flask best practices:

- **Blueprint Organization**: Modular route organization
- **SQLAlchemy ORM**: Database abstraction and management
- **CORS Support**: Cross-origin request handling
- **Error Handling**: Comprehensive error management and logging

### Testing

Run tests for both frontend and backend:

```bash
# Frontend tests
cd confiflow-ui
pnpm test

# Backend tests
cd confiflow-backend
source venv/bin/activate
python -m pytest
```

## 🚀 Deployment

### Production Deployment

#### Frontend (Static Hosting)
Deploy to platforms like Netlify, Vercel, or Firebase Hosting:

```bash
cd confiflow-ui
pnpm run build
# Deploy the dist/ directory
```

#### Backend (Server Deployment)
Deploy using Docker, cloud platforms, or traditional servers:

```bash
cd confiflow-backend
# Configure production environment
# Deploy using your preferred method
```

### Docker Deployment

Use the provided Docker configurations for containerized deployment:

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

We welcome contributions to ConfiFlow! Please follow these guidelines:

1. **Fork the Repository**: Create your own fork of the project
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**: Submit a pull request for review

### Development Guidelines

- Follow existing code style and conventions
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

ConfiFlow is built upon the foundation of numerous open-source projects and technologies:

- **React** - User interface library
- **Flask** - Web framework for Python
- **Tailwind CSS** - Utility-first CSS framework
- **Ollama** - Local LLM platform
- **N8N** - Workflow automation platform
- **Whisper** - Speech recognition model
- **Tesseract** - OCR engine
- **Pandoc** - Universal document converter

## 📞 Support

For support, questions, or feature requests:

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/confiflow/issues)
- **Documentation**: Check the `/docs` directory for detailed guides
- **Community**: Join our community discussions

## 🔮 Roadmap

### Upcoming Features

- **Enhanced AI Models**: Support for additional local and cloud-based AI services
- **Advanced Analytics**: Comprehensive research analytics and insights
- **Collaboration Tools**: Multi-user support and real-time collaboration
- **Plugin System**: Extensible architecture for custom integrations
- **Mobile Applications**: Native mobile apps for iOS and Android

### Version History

- **v1.0.0** - Initial release with core functionality
- **v0.9.0** - Beta release with AI integration
- **v0.8.0** - Alpha release with basic workflow automation

---

**Made with ❤️ by Ashwini Kumar Tarai**

*ConfiFlow - Empowering researchers and writers with open-source AI technology*

