import os
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.parse import urljoin


class VercelBlobStorage(Storage):
    """
    Custom storage backend for Vercel Blob Storage
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'VERCEL_BLOB_BASE_URL', 'https://yryhdmorv8znchlu.public.blob.vercel-storage.com')
        self.token = getattr(settings, 'BLOB_READ_WRITE_TOKEN', '')
    
    def _save(self, name, content):
        """
        Save file to Vercel Blob Storage
        """
        # Read file content
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content
            
        # Upload to Vercel Blob Storage
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/octet-stream'
        }
        
        upload_url = f"https://blob.vercel-storage.com/upload"
        
        response = requests.put(
            upload_url,
            data=file_content,
            headers=headers,
            params={'filename': name}
        )
        
        if response.status_code == 200:
            return name
        else:
            raise Exception(f"Failed to upload file: {response.text}")
    
    def _open(self, name, mode='rb'):
        """
        Open file from Vercel Blob Storage
        """
        url = self.url(name)
        response = requests.get(url)
        if response.status_code == 200:
            return ContentFile(response.content)
        else:
            raise FileNotFoundError(f"File {name} not found")
    
    def delete(self, name):
        """
        Delete file from Vercel Blob Storage
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        
        delete_url = f"https://blob.vercel-storage.com/delete"
        response = requests.delete(
            delete_url,
            headers=headers,
            params={'url': self.url(name)}
        )
        
        return response.status_code == 200
    
    def exists(self, name):
        """
        Check if file exists
        """
        try:
            url = self.url(name)
            response = requests.head(url)
            return response.status_code == 200
        except:
            return False
    
    def listdir(self, path):
        """
        List directory contents (not implemented for blob storage)
        """
        return [], []
    
    def size(self, name):
        """
        Get file size
        """
        try:
            url = self.url(name)
            response = requests.head(url)
            return int(response.headers.get('Content-Length', 0))
        except:
            return 0
    
    def url(self, name):
        """
        Get public URL for file
        """
        return urljoin(self.base_url + '/', name)
    
    def get_accessed_time(self, name):
        """
        Get last accessed time (not supported)
        """
        raise NotImplementedError("Vercel Blob Storage doesn't support accessed time")
    
    def get_created_time(self, name):
        """
        Get created time (not supported)
        """
        raise NotImplementedError("Vercel Blob Storage doesn't support created time")
    
    def get_modified_time(self, name):
        """
        Get modified time (not supported)
        """
        raise NotImplementedError("Vercel Blob Storage doesn't support modified time")
