import os
from dotenv import load_dotenv

from AzureHelper.azure_helper import AzureHelper
from Scraper.vpn_gate_scraper import VpnGateScraper

load_dotenv()

if __name__ == '__main__':
    azure_conn_string = os.getenv('AZURE_BLOB_CONN_STRING')
    azure_blob_container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')

    scraper = VpnGateScraper()

    ovpn_files = scraper.scrape_ovpn_files(10)
    
    azure_helper = AzureHelper(azure_conn_string)

    for index, file_content in enumerate(ovpn_files):
        filename = index+1
        
        azure_helper.upload_ovpnblobs_to_container(azure_blob_container_name, file_content, filename)

    