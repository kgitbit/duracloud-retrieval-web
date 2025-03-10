"""
DuraCloud Content Retrieval Tool
Copyright 2024 Krishna Pareek

This work is a derivative of DuraCloud, Copyright 2009-2019 DuraSpace.
Licensed under the Apache License, Version 2.0
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import re
import platform
import tempfile
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='frontend')

# Configuration from environment variables
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'duracloud-uploads')
ALLOWED_EXTENSIONS = {'txt'}
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT', 5000))
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', os.path.join(os.getcwd(), 'downloads'))

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not HOST:
    raise ValueError("HOST environment variable must be configured with your institution's DuraCloud host")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_output(output_text):
    """Parse the command output to extract file statuses."""
    files = []
    lines = output_text.split('\n')
    
    for line in lines:
        if 'Downloading file:' in line:
            file_name = line.split('Downloading file:')[-1].strip()
            files.append({
                'name': file_name,
                'status': 'pending',
                'message': 'Starting download...'
            })
        elif 'Successfully downloaded file:' in line:
            file_name = line.split('Successfully downloaded file:')[-1].strip()
            files.append({
                'name': file_name,
                'status': 'success',
                'message': f'Downloaded to {DOWNLOAD_DIR}'
            })
        elif 'Error downloading file:' in line:
            match = re.search(r'Error downloading file: (.*?) - (.*)', line)
            if match:
                file_name, error = match.groups()
                files.append({
                    'name': file_name,
                    'status': 'error',
                    'message': error
                })

    return files

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/config')
def get_config():
    """Endpoint to get configuration for the frontend."""
    return jsonify({
        'defaultHost': HOST,
        'defaultDownloadDir': '/downloads',
        'platform': platform.system()
    })

@app.route('/history')
def get_history():
    """Endpoint to get download history."""
    return jsonify({
        'message': 'History feature coming soon!'
    })

@app.route('/download', methods=['POST'])
def download_content():
    try:
        # Get form data
        host = request.form.get('host', HOST)
        username = request.form['username']
        password = request.form['password']
        space = request.form['space']
        
        # Handle file upload
        if 'contentList' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['contentList']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Construct and execute command
            command = [
                'java', '-jar', 'retrievaltool-8.0.0-driver.jar',
                '-h', host,
                '-u', username,
                '-p', password,
                '-s', space,
                '-c', DOWNLOAD_DIR,
                '--list-file', filepath
            ]
            
            # Execute command
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if process.returncode == 0:
                # Parse the output to get file statuses
                files = parse_output(stdout)
                return jsonify({
                    'status': 'success',
                    'message': f'All downloads completed successfully. Files saved to downloads directory.',
                    'files': files,
                    'output': stdout
                })
            else:
                # Try to parse any output even in case of error
                files = parse_output(stdout)
                return jsonify({
                    'status': 'error',
                    'message': 'Error during download process',
                    'files': files,
                    'error': stderr
                }), 500
                
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True) 