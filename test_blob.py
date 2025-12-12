import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

try:
    # Get connection string from .env
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    
    # Connect
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    
    # List containers
    containers = list(blob_service_client.list_containers())
    
    print("✅ Blob Storage connection successful!")
    print(f"Found {len(containers)} containers")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
