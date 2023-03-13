import os

from azure.storage.blob import BlobServiceClient


class AzureHelper:

    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
    
    def upload_ovpnblobs_to_container(self, container_name, file_content, filename):

        # Create a local directory to hold blob data
        local_path = "./data"
        if not os.path.isdir(local_path): os.mkdir(local_path)

        # Create a file in the local data directory to upload and download
        local_file_name = str(filename) + ".ovpn"
        upload_file_path = os.path.join(local_path, local_file_name)

        # Write text to the file
        file = open(file=upload_file_path, mode='w')
        file.write(file_content)
        file.close()

        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(file=upload_file_path, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)   