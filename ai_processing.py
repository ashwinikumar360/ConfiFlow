from flask import Blueprint, request, jsonify
import requests
import os
import subprocess
import tempfile
from werkzeug.utils import secure_filename

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ollama/generate', methods=['POST'])
def ollama_generate():
    """
    Endpoint to interact with local Ollama instance for text generation.
    Expects JSON payload with 'model' and 'prompt' fields.
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request'}), 400
        
        model = data.get('model', 'llama3')
        prompt = data.get('prompt')
        
        # Default Ollama API endpoint
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
        
        payload = {
            'model': model,
            'prompt': prompt,
            'stream': False
        }
        
        response = requests.post(ollama_url, json=payload, timeout=120)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Ollama API error', 'details': response.text}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to Ollama', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@ai_bp.route('/whisper/transcribe', methods=['POST'])
def whisper_transcribe():
    """
    Endpoint to transcribe audio files using Whisper.
    Expects multipart/form-data with audio file.
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(audio_file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Run Whisper transcription
            result = subprocess.run([
                'whisper', temp_path, '--model', 'base', '--output_format', 'txt'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Read transcription result
                txt_path = temp_path.replace(os.path.splitext(temp_path)[1], '.txt')
                if os.path.exists(txt_path):
                    with open(txt_path, 'r') as f:
                        transcription = f.read().strip()
                    os.unlink(txt_path)  # Clean up
                    return jsonify({'transcription': transcription})
                else:
                    return jsonify({'error': 'Transcription file not found'}), 500
            else:
                return jsonify({'error': 'Whisper transcription failed', 'details': result.stderr}), 500
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Transcription timeout'}), 408
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@ai_bp.route('/document/extract', methods=['POST'])
def extract_document_text():
    """
    Endpoint to extract text from various document formats (PDF, DOCX).
    Expects multipart/form-data with document file.
    """
    try:
        if 'document' not in request.files:
            return jsonify({'error': 'No document file provided'}), 400
        
        doc_file = request.files['document']
        if doc_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(doc_file.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            doc_file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            extracted_text = ""
            
            if file_ext == '.pdf':
                # Extract text from PDF using pdftotext
                result = subprocess.run([
                    'pdftotext', temp_path, '-'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    extracted_text = result.stdout
                else:
                    return jsonify({'error': 'PDF text extraction failed', 'details': result.stderr}), 500
                    
            elif file_ext == '.docx':
                # Extract text from DOCX using pandoc
                result = subprocess.run([
                    'pandoc', temp_path, '-t', 'plain'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    extracted_text = result.stdout
                else:
                    return jsonify({'error': 'DOCX text extraction failed', 'details': result.stderr}), 500
            else:
                return jsonify({'error': f'Unsupported file format: {file_ext}'}), 400
            
            return jsonify({'extracted_text': extracted_text.strip()})
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@ai_bp.route('/tts/generate', methods=['POST'])
def generate_speech():
    """
    Endpoint to generate speech from text using Festival TTS.
    Expects JSON payload with 'text' field.
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text in request'}), 400
        
        text = data.get('text')
        
        # Generate speech using Festival
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_path = temp_file.name
        
        try:
            # Use Festival to generate speech
            result = subprocess.run([
                'echo', text
            ], stdout=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                festival_result = subprocess.run([
                    'festival', '--tts'
                ], input=text, capture_output=True, text=True)
                
                if festival_result.returncode == 0:
                    return jsonify({'message': 'Speech generated successfully'})
                else:
                    return jsonify({'error': 'Festival TTS failed', 'details': festival_result.stderr}), 500
            else:
                return jsonify({'error': 'Text processing failed'}), 500
                
        finally:
            # Clean up temporary file if it exists
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

