# ConfiFlow Project Structure

**Author**: Ashwini Kumar Tarai  
**Last Updated**: June 26, 2025

This document outlines the complete structure of the ConfiFlow project, providing an overview of all directories, files, and their purposes.

## Root Directory Structure

```
ConfiFlow/
├── confiflow-ui/                 # React Frontend Application
├── confiflow-backend/            # Flask Backend API
├── docs/                         # Documentation files
├── README.md                     # Main project documentation
├── INSTALLATION.md               # Installation instructions
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
├── .env.example                  # Environment variables template
├── docker-compose.yml            # Docker deployment configuration
└── PROJECT_STRUCTURE.md          # This file
```

## Frontend Structure (confiflow-ui/)

```
confiflow-ui/
├── public/                       # Static assets served directly
│   ├── favicon.ico              # Application favicon
│   └── index.html               # Main HTML template
├── src/                         # Source code
│   ├── assets/                  # Images, logos, and static media
│   ├── components/              # Reusable React components
│   │   └── ui/                  # UI components (shadcn/ui)
│   ├── hooks/                   # Custom React hooks
│   ├── lib/                     # Utility functions and libraries
│   ├── App.css                  # Application-specific styles
│   ├── App.jsx                  # Main application component
│   ├── index.css                # Global styles and Tailwind imports
│   └── main.jsx                 # React application entry point
├── components.json              # shadcn/ui configuration
├── eslint.config.js             # ESLint configuration
├── index.html                   # Vite HTML template
├── package.json                 # Node.js dependencies and scripts
├── pnpm-lock.yaml              # Package manager lock file
├── vite.config.js              # Vite bundler configuration
└── frontend_documentation.md    # Frontend-specific documentation
```

## Backend Structure (confiflow-backend/)

```
confiflow-backend/
├── src/                         # Source code
│   ├── models/                  # Database models
│   │   └── user.py             # User model definition
│   ├── routes/                  # API route definitions
│   │   ├── user.py             # User management routes
│   │   ├── ai_processing.py    # AI integration endpoints
│   │   └── n8n_integration.py  # N8N workflow endpoints
│   ├── static/                 # Static file serving directory
│   ├── database/               # Database files
│   │   └── app.db              # SQLite database file
│   └── main.py                 # Flask application entry point
├── venv/                       # Python virtual environment
├── requirements.txt            # Python dependencies
└── backend_documentation.md    # Backend-specific documentation
```

## Documentation Structure

```
docs/
├── api/                        # API documentation
│   ├── ai_endpoints.md         # AI processing API docs
│   ├── n8n_endpoints.md        # N8N integration API docs
│   └── user_endpoints.md       # User management API docs
├── deployment/                 # Deployment guides
│   ├── docker.md              # Docker deployment guide
│   ├── production.md           # Production deployment guide
│   └── cloud.md               # Cloud deployment options
├── development/                # Development guides
│   ├── frontend.md             # Frontend development guide
│   ├── backend.md              # Backend development guide
│   └── testing.md              # Testing guidelines
└── user_guides/               # User documentation
    ├── getting_started.md      # Getting started guide
    ├── features.md             # Feature documentation
    └── troubleshooting.md      # Common issues and solutions
```

## Configuration Files

### Environment Configuration
- `.env.example` - Template for environment variables
- `.env` - Local environment variables (not in version control)

### Docker Configuration
- `docker-compose.yml` - Multi-service Docker setup
- `Dockerfile` - Container build instructions (in each service directory)

### Development Configuration
- `.gitignore` - Git ignore patterns
- `eslint.config.js` - JavaScript linting rules
- `vite.config.js` - Frontend build configuration

## Key Features by Directory

### Frontend Features (`confiflow-ui/`)
- **React 18** with modern hooks and functional components
- **Tailwind CSS** for utility-first styling
- **Lucide React** for beautiful icons
- **Vite** for fast development and building
- **shadcn/ui** for consistent UI components

### Backend Features (`confiflow-backend/`)
- **Flask** web framework with Blueprint organization
- **SQLAlchemy** ORM for database operations
- **Flask-CORS** for cross-origin request handling
- **AI Integration** endpoints for various AI services
- **N8N Integration** for workflow automation

### AI Processing Capabilities
- **Ollama Integration** - Local language model support
- **Whisper Integration** - Audio transcription
- **Document Processing** - PDF and DOCX text extraction
- **Text-to-Speech** - Festival TTS integration

### Workflow Automation
- **N8N Webhooks** - Trigger workflows from the application
- **Workflow Management** - List and execute workflows
- **Execution Monitoring** - Track workflow progress

## File Naming Conventions

### Frontend
- **Components**: PascalCase (e.g., `UserProfile.jsx`)
- **Hooks**: camelCase with "use" prefix (e.g., `useApiClient.js`)
- **Utilities**: camelCase (e.g., `formatDate.js`)
- **Styles**: kebab-case (e.g., `app-styles.css`)

### Backend
- **Routes**: snake_case (e.g., `ai_processing.py`)
- **Models**: snake_case (e.g., `user_model.py`)
- **Utilities**: snake_case (e.g., `file_utils.py`)
- **Configuration**: UPPER_CASE (e.g., `CONFIG.py`)

## Development Workflow

### Frontend Development
1. Navigate to `confiflow-ui/`
2. Install dependencies: `pnpm install`
3. Start development server: `pnpm run dev`
4. Build for production: `pnpm run build`

### Backend Development
1. Navigate to `confiflow-backend/`
2. Activate virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start development server: `python src/main.py`

### Full Stack Development
1. Use Docker Compose: `docker-compose up -d`
2. Or run both frontend and backend separately
3. Configure environment variables as needed

## Deployment Structure

### Development
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:5000`
- N8N: `http://localhost:5678`
- Ollama: `http://localhost:11434`

### Production
- All services behind reverse proxy
- SSL/TLS termination
- Database persistence
- Log aggregation
- Monitoring and alerting

## Security Considerations

### File Permissions
- Configuration files: `600` (owner read/write only)
- Application files: `644` (owner read/write, group/other read)
- Executable files: `755` (owner read/write/execute, group/other read/execute)

### Sensitive Data
- Environment variables for secrets
- Database credentials in secure storage
- API keys in environment configuration
- SSL certificates in protected directories

## Maintenance

### Regular Updates
- Node.js dependencies: `pnpm update`
- Python dependencies: `pip install -U -r requirements.txt`
- System packages: `apt update && apt upgrade`
- AI models: `ollama pull <model-name>`

### Backup Procedures
- Database backups: Regular automated backups
- Configuration backups: Version controlled
- User data backups: Scheduled file system backups
- Documentation updates: Keep in sync with code changes

---

**Author**: Ashwini Kumar Tarai  
**Note**: This structure is designed for scalability and maintainability. As the project grows, additional directories and organization patterns may be introduced while maintaining the core architectural principles.

