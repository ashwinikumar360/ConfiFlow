from flask import Blueprint, request, jsonify
import requests
import os
import json

n8n_bp = Blueprint('n8n', __name__)

@n8n_bp.route('/webhook/<workflow_id>', methods=['POST'])
def trigger_n8n_workflow(workflow_id):
    """
    Endpoint to trigger N8N workflows via webhook.
    Forwards the request payload to the specified N8N workflow.
    """
    try:
        # Get N8N instance URL from environment variable
        n8n_base_url = os.getenv('N8N_URL', 'http://localhost:5678')
        
        # Construct webhook URL
        webhook_url = f"{n8n_base_url}/webhook/{workflow_id}"
        
        # Forward the request data to N8N
        data = request.get_json() if request.is_json else request.form.to_dict()
        headers = {
            'Content-Type': 'application/json' if request.is_json else 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(webhook_url, json=data if request.is_json else None, 
                               data=data if not request.is_json else None, 
                               headers=headers, timeout=300)
        
        if response.status_code == 200:
            try:
                return jsonify(response.json())
            except json.JSONDecodeError:
                return jsonify({'message': response.text})
        else:
            return jsonify({
                'error': 'N8N workflow execution failed',
                'status_code': response.status_code,
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to N8N', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@n8n_bp.route('/workflows', methods=['GET'])
def list_workflows():
    """
    Endpoint to list available N8N workflows.
    Requires N8N API access.
    """
    try:
        n8n_base_url = os.getenv('N8N_URL', 'http://localhost:5678')
        api_key = os.getenv('N8N_API_KEY')
        
        if not api_key:
            return jsonify({'error': 'N8N API key not configured'}), 500
        
        headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{n8n_base_url}/api/v1/workflows", headers=headers, timeout=30)
        
        if response.status_code == 200:
            workflows = response.json()
            return jsonify({
                'workflows': [
                    {
                        'id': workflow['id'],
                        'name': workflow['name'],
                        'active': workflow['active']
                    }
                    for workflow in workflows.get('data', [])
                ]
            })
        else:
            return jsonify({
                'error': 'Failed to fetch workflows',
                'status_code': response.status_code,
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to N8N API', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@n8n_bp.route('/workflow/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """
    Endpoint to execute N8N workflow directly via API.
    Requires N8N API access.
    """
    try:
        n8n_base_url = os.getenv('N8N_URL', 'http://localhost:5678')
        api_key = os.getenv('N8N_API_KEY')
        
        if not api_key:
            return jsonify({'error': 'N8N API key not configured'}), 500
        
        headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        # Get input data from request
        input_data = request.get_json() or {}
        
        # Execute workflow
        execution_data = {
            'workflowData': {
                'id': workflow_id
            },
            'inputData': input_data
        }
        
        response = requests.post(
            f"{n8n_base_url}/api/v1/workflows/{workflow_id}/execute",
            json=execution_data,
            headers=headers,
            timeout=300
        )
        
        if response.status_code == 200:
            execution_result = response.json()
            return jsonify({
                'execution_id': execution_result.get('data', {}).get('executionId'),
                'status': 'started',
                'message': 'Workflow execution initiated'
            })
        else:
            return jsonify({
                'error': 'Workflow execution failed',
                'status_code': response.status_code,
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to N8N API', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@n8n_bp.route('/execution/<execution_id>/status', methods=['GET'])
def get_execution_status(execution_id):
    """
    Endpoint to check the status of an N8N workflow execution.
    """
    try:
        n8n_base_url = os.getenv('N8N_URL', 'http://localhost:5678')
        api_key = os.getenv('N8N_API_KEY')
        
        if not api_key:
            return jsonify({'error': 'N8N API key not configured'}), 500
        
        headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{n8n_base_url}/api/v1/executions/{execution_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            execution_data = response.json()
            return jsonify({
                'execution_id': execution_id,
                'status': execution_data.get('data', {}).get('finished') and 'completed' or 'running',
                'start_time': execution_data.get('data', {}).get('startedAt'),
                'end_time': execution_data.get('data', {}).get('stoppedAt'),
                'data': execution_data.get('data', {})
            })
        else:
            return jsonify({
                'error': 'Failed to fetch execution status',
                'status_code': response.status_code,
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to N8N API', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

