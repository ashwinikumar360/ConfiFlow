# ConfiFlow Backend - API Documentation

This document provides comprehensive documentation for the ConfiFlow Backend API, which serves as the core processing engine for the ConfiFlow research and writing assistant platform.

## 1. Overview

The ConfiFlow Backend is built using Flask, a lightweight and flexible Python web framework that provides the foundation for creating robust web applications and APIs. This backend serves multiple critical functions within the ConfiFlow ecosystem, acting as the bridge between the user interface and various AI processing capabilities, document handling systems, and workflow automation tools.

The architecture follows a modular blueprint-based approach, where different functionalities are organized into separate route modules. This design pattern promotes code maintainability, scalability, and clear separation of concerns. The backend integrates with several open-source technologies and services to provide a comprehensive suite of features for research, document processing, and content generation.

## 2. Architecture and Technologies

### 2.1. Core Framework

The backend leverages Flask as its primary web framework, chosen for its simplicity, flexibility, and extensive ecosystem. Flask provides the essential components needed for building web applications, including routing, request handling, templating, and session management. The framework's minimalist approach allows for precise control over the application structure while maintaining the ability to scale and extend functionality as needed.

### 2.2. Database Integration

The application utilizes SQLAlchemy as its Object-Relational Mapping (ORM) tool, providing a high-level abstraction for database operations. SQLite serves as the default database engine, offering a lightweight, serverless database solution that requires minimal configuration and maintenance. This choice makes the application highly portable and suitable for both development and small to medium-scale production deployments.

The database configuration is designed to be easily adaptable to other database systems such as PostgreSQL or MySQL by simply modifying the connection string in the application configuration. This flexibility ensures that the application can grow and adapt to different deployment scenarios and performance requirements.

### 2.3. Cross-Origin Resource Sharing (CORS)

To enable seamless communication between the frontend and backend components, the application implements CORS support through the Flask-CORS extension. This configuration allows the React frontend to make API requests to the backend from different origins, which is essential for modern web application architectures where frontend and backend services may be deployed on different domains or ports.

## 3. API Endpoints and Functionality

### 3.1. AI Processing Endpoints

The AI processing module provides several endpoints for integrating with various artificial intelligence and machine learning services. These endpoints are designed to handle different types of content processing tasks that are central to the ConfiFlow platform's functionality.

#### 3.1.1. Ollama Integration

The `/api/ai/ollama/generate` endpoint provides integration with Ollama, an open-source platform for running large language models locally. This endpoint accepts POST requests with JSON payloads containing a prompt and optionally a model specification. The integration allows users to leverage powerful language models for text generation, summarization, question answering, and other natural language processing tasks without relying on external cloud services.

The endpoint handles various error scenarios, including connection failures, timeout issues, and invalid requests. It provides comprehensive error reporting to help diagnose and resolve integration issues. The default timeout is set to 120 seconds to accommodate the processing time required for complex language model operations.

#### 3.1.2. Audio Transcription

The `/api/ai/whisper/transcribe` endpoint integrates with OpenAI's Whisper model for automatic speech recognition. This endpoint accepts multipart form data containing audio files and returns transcribed text. The implementation uses the command-line Whisper tool, which must be installed on the system running the backend.

The transcription process involves temporarily storing the uploaded audio file, processing it through Whisper, and returning the resulting text. The endpoint includes proper file handling and cleanup procedures to ensure system resources are managed efficiently. Support for various audio formats depends on the underlying Whisper installation and its dependencies.

#### 3.1.3. Document Text Extraction

The `/api/ai/document/extract` endpoint provides text extraction capabilities for various document formats, including PDF and DOCX files. This functionality is essential for processing research materials, academic papers, and other documents that users may want to analyze or incorporate into their work.

For PDF files, the endpoint utilizes the `pdftotext` utility from the Poppler suite, which provides reliable and efficient text extraction capabilities. For DOCX files, the implementation uses Pandoc, a universal document converter that can handle various document formats and convert them to plain text while preserving the essential content structure.

#### 3.1.4. Text-to-Speech Generation

The `/api/ai/tts/generate` endpoint provides text-to-speech functionality using the Festival Speech Synthesis System. This endpoint accepts JSON payloads containing text and generates spoken audio output. While the current implementation provides basic TTS capabilities, it can be extended to support more advanced speech synthesis systems like Coqui TTS for higher quality output.

### 3.2. N8N Workflow Integration

The N8N integration module provides comprehensive support for workflow automation through the N8N platform. N8N is an open-source workflow automation tool that allows users to create complex data processing pipelines and integrate various services and APIs.

#### 3.2.1. Webhook Triggers

The `/api/n8n/webhook/<workflow_id>` endpoint serves as a bridge between the ConfiFlow application and N8N workflows. This endpoint accepts POST requests and forwards them to the corresponding N8N webhook, enabling seamless integration between user actions in the ConfiFlow interface and automated workflow execution.

The implementation handles both JSON and form data payloads, ensuring compatibility with various types of workflow triggers. Error handling includes proper status code forwarding and detailed error reporting to help diagnose workflow execution issues.

#### 3.2.2. Workflow Management

The `/api/n8n/workflows` endpoint provides access to the list of available N8N workflows through the N8N API. This functionality requires proper API key configuration and enables the ConfiFlow interface to display available workflows to users. The endpoint returns essential workflow information including ID, name, and activation status.

#### 3.2.3. Direct Workflow Execution

The `/api/n8n/workflow/<workflow_id>/execute` endpoint allows for direct execution of N8N workflows through the API rather than webhook triggers. This approach provides more control over workflow execution and enables the passing of structured input data to workflows.

#### 3.2.4. Execution Monitoring

The `/api/n8n/execution/<execution_id>/status` endpoint provides real-time monitoring of workflow execution status. This functionality is crucial for long-running workflows where users need to track progress and receive notifications when processing is complete.

## 4. Configuration and Environment Variables

The backend application relies on several environment variables for configuration, allowing for flexible deployment across different environments without code modifications.

### 4.1. AI Service Configuration

- `OLLAMA_URL`: Specifies the URL for the Ollama API endpoint (default: http://localhost:11434/api/generate)
- `N8N_URL`: Defines the base URL for the N8N instance (default: http://localhost:5678)
- `N8N_API_KEY`: Authentication key for N8N API access (required for workflow management features)

### 4.2. Security Configuration

The application includes a secret key configuration for session management and security features. In production deployments, this should be set to a strong, randomly generated value and kept secure.

## 5. Development Setup and Installation

### 5.1. Prerequisites

The backend requires Python 3.11 or later and several system-level dependencies for document processing and AI integration. Essential system packages include:

- `poppler-utils` for PDF text extraction
- `pandoc` for document format conversion
- `festival` for text-to-speech functionality
- `whisper` for audio transcription (can be installed via pip)

### 5.2. Virtual Environment Setup

The project uses a Python virtual environment to manage dependencies and ensure consistent deployment across different systems. The virtual environment is created and activated using standard Python tools, and all project dependencies are installed within this isolated environment.

### 5.3. Dependency Management

All Python dependencies are managed through pip and documented in the `requirements.txt` file. This approach ensures reproducible deployments and simplifies dependency management across different environments.

## 6. Deployment Considerations

### 6.1. Production Configuration

For production deployments, several configuration changes are recommended:

- Use a production-grade WSGI server such as Gunicorn or uWSGI instead of the Flask development server
- Configure proper logging and monitoring
- Set up SSL/TLS encryption for secure communication
- Use environment-specific configuration files
- Implement proper error handling and user feedback mechanisms

### 6.2. Scalability

The modular architecture of the backend allows for horizontal scaling by deploying multiple instances behind a load balancer. Database connections can be pooled and managed efficiently to handle increased load. For high-traffic scenarios, consider migrating from SQLite to a more robust database system like PostgreSQL.

### 6.3. Security

Security considerations include proper input validation, secure file handling, authentication and authorization mechanisms, and protection against common web vulnerabilities. The CORS configuration should be restricted to specific origins in production environments.

---

**Author**: Ashwini Kumar Tarai
**Date**: June 26, 2025

