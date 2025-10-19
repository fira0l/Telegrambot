import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/documents'
]

class GoogleDriveManager:
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.folder_id = None
        self.doc_id = None
        self.authenticate()
    
    def authenticate(self):
        creds = None
        
        # Load existing credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=8080)
            
            # Save credentials
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        # Build services directly with credentials
        self.drive_service = build('drive', 'v3', credentials=creds)
        self.docs_service = build('docs', 'v1', credentials=creds)
        self.ensure_portfolio_folder()
        self.ensure_portfolio_document()
    
    def ensure_portfolio_folder(self):
        # Check if portfolio folder exists
        results = self.drive_service.files().list(
            q="name='Portfolio Images' and mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            self.folder_id = folders[0]['id']
        else:
            # Create portfolio folder
            folder_metadata = {
                'name': 'Portfolio Images',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
            self.folder_id = folder.get('id')
    
    def ensure_portfolio_document(self):
        try:
            print("Checking for Portfolio Metadata document...")
            # Check if portfolio metadata document exists
            results = self.drive_service.files().list(
                q="name='Portfolio Metadata' and mimeType='application/vnd.google-apps.document'",
                fields="files(id, name)"
            ).execute()
            
            docs = results.get('files', [])
            
            if docs:
                self.doc_id = docs[0]['id']
                print(f"Found existing document: {self.doc_id}")
            else:
                print("Creating new Portfolio Metadata document...")
                # Create portfolio metadata document
                doc_metadata = {
                    'name': 'Portfolio Metadata',
                    'mimeType': 'application/vnd.google-apps.document'
                }
                doc = self.drive_service.files().create(body=doc_metadata, fields='id').execute()
                self.doc_id = doc.get('id')
                print(f"Created document: {self.doc_id}")
                
                # Initialize document with header
                requests = [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': 'Portfolio Metadata\n\n'
                    }
                }]
                self.docs_service.documents().batchUpdate(
                    documentId=self.doc_id,
                    body={'requests': requests}
                ).execute()
                print("Document initialized with header")
        except Exception as e:
            print(f"Error ensuring document: {e}")
            import traceback
            traceback.print_exc()
    
    def upload_image_from_memory(self, file_content, filename, title):
        try:
            print(f"Starting memory upload for: {title}")
            
            # Detect file type from filename
            import mimetypes
            mime_type, _ = mimetypes.guess_type(filename)
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/jpeg'
            
            # Get file extension
            ext = os.path.splitext(filename)[1] or '.jpg'
            
            file_metadata = {
                'name': f"{title}{ext}",
                'parents': [self.folder_id]
            }
            
            # Use BytesIO for memory upload
            from io import BytesIO
            from googleapiclient.http import MediaIoBaseUpload
            
            file_buffer = BytesIO(file_content)
            media = MediaIoBaseUpload(file_buffer, mimetype=mime_type, resumable=True, chunksize=1024*512)
            
            # Retry upload with exponential backoff
            import time
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"Upload attempt {attempt + 1}/{max_retries}")
                    file = self.drive_service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id,webViewLink,webContentLink'
                    ).execute()
                    break
                except Exception as retry_error:
                    print(f"Attempt {attempt + 1} failed: {retry_error}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2 ** attempt)  # Exponential backoff
                    file_buffer.seek(0)  # Reset buffer position
            
            print(f"File uploaded with ID: {file.get('id')}")
            
            # Make file publicly viewable
            self.drive_service.permissions().create(
                fileId=file.get('id'),
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            print("File made public")
            
            # Add metadata to document
            print(f"Adding to document: {self.doc_id}")
            self.add_to_document(file.get('id'), title)
            
            # Get direct image URL
            image_url = f"https://drive.google.com/uc?id={file.get('id')}"
            
            return {
                'id': file.get('id'),
                'url': image_url,
                'title': title
            }
        except Exception as e:
            print(f"Upload error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def add_to_document(self, file_id, title):
        try:
            print(f"Getting document: {self.doc_id}")
            # Get current document content
            doc = self.docs_service.documents().get(documentId=self.doc_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            print(f"Document content length: {len(content)}")
            
            # Find the end of the document
            end_index = 1
            for element in content:
                if 'endIndex' in element:
                    end_index = element['endIndex']
            
            print(f"End index: {end_index}")
            
            # Add new entry
            entry_text = f"Title: {title}\nFile ID: {file_id}\nURL: https://drive.google.com/uc?id={file_id}\n\n"
            
            requests = [{
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': entry_text
                }
            }]
            
            print(f"Updating document with text: {entry_text[:50]}...")
            
            result = self.docs_service.documents().batchUpdate(
                documentId=self.doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"Document updated successfully: {result}")
            
        except Exception as e:
            print(f"Document update error: {e}")
            import traceback
            traceback.print_exc()
    
    def get_all_images(self):
        try:
            results = self.drive_service.files().list(
                q=f"'{self.folder_id}' in parents and mimeType contains 'image/'",
                fields="files(id, name, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            images = []
            
            for file in files:
                images.append({
                    'id': file['id'],
                    'title': file['name'].replace('.jpg', '').replace('.png', '').replace('.jpeg', ''),
                    'src': f"https://drive.google.com/uc?id={file['id']}"
                })
            
            return images
        except Exception as e:
            print(f"Fetch error: {e}")
            return []