from azure.storage.blob import BlobServiceClient

# Connection string to your Azure Storage account
connection_string = "your_connection_string"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Name of the container and blob
container_name = "your-container-name"
blob_name = "your-blob-name"

# Data to upload
blob_data = b"Hello, Azure Blob Storage!"

# Metadata for the blob
metadata = {
    "key1": "value1",
    "key2": "value2"
}

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# Ensure the container exists
if not container_client.exists():
    container_client.create_container()

# Upload the blob with metadata
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(blob_data, metadata=metadata, overwrite=True)

print(f"Blob '{blob_name}' uploaded to container '{container_name}' with metadata {metadata}.")
