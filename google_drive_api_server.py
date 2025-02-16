import os
import json
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)

# Google Drive API Credentials from Environment Variable or File
SERVICE_ACCOUNT_INFO = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
SERVICE_ACCOUNT_FILE = 'credentials/hea-ai-drive-key.json'  # Local file fallback
SCOPES = ['https://www.googleapis.com/auth/drive']

if SERVICE_ACCOUNT_INFO:
    creds = service_account.Credentials.from_service_account_info(json.loads(SERVICE_ACCOUNT_INFO), scopes=SCOPES)
elif os.path.exists(SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
else:
    raise Exception("Missing Google Drive API credentials. Set GOOGLE_APPLICATION_CREDENTIALS_JSON or ensure the service account file exists.")

# Initialize Google Drive API client
service = build('drive', 'v3', credentials=creds)

@app.route('/list-files', methods=['GET'])
def list_files():
    """ List files in Google Drive folder """
    folder_id = request.args.get('folder_id', '')  # Provide folder ID as query parameter
    if not folder_id:
        return jsonify({"error": "Missing folder_id parameter"}), 400
    
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    return jsonify(results.get('files', []))

@app.route('/upload-file', methods=['POST'])
def upload_file():
    """ Upload a file to Google Drive """
    data = request.json
    file_name = data.get('file_name', 'test.txt')
    folder_id = data.get('folder_id', '')

    if not folder_id:
        return jsonify({"error": "Missing folder_id"}), 400
    
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_name, mimetype='text/plain')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return jsonify({"file_id": file.get('id')})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Ensure Cloud Run uses the correct port
    app.run(host="0.0.0.0", port=port)
