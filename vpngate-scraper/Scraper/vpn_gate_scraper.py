import base64
import re
import requests
from bs4 import BeautifulSoup


class VpnGateScraper:

    def __init__(self):
        # URL of site allocated to scraping
        self.url = 'http://www.vpngate.net/api/iphone/'
        self.page = requests.get(self.url)

    def append_additional_required_vpn_configurations(self, file_in_string_format):
        heading_of_place_to_update = '# It is not recommended to modify it unless you have a particular need.'
        new_file_array = []   
    
        layer_of_connection = None
        cipher_fallback = None
        new_line = None

        layer_key = 'dev'
        cipher_key = 'cipher'

        for line in file_in_string_format.split('\n'):

            if (layer_of_connection is None 
                and self.is_layer_of_vpn_connection(line, layer_key)):
                layer_of_connection = line

            if (cipher_fallback is None 
                and self.is_cipher(line, cipher_key)):
                cipher_fallback = self.convert_cipher_to_fallback(line, cipher_key)

            if (layer_of_connection
                and cipher_fallback
                and new_line is None # Prevents going through this once we attain the new line
                and line.strip() == heading_of_place_to_update):
                additional_required_configurations = f'\n\n{layer_of_connection}{cipher_fallback}'
                
                new_line = line + additional_required_configurations

                new_file_array.append(new_line)
                continue

            new_file_array.append(line)

        new_file = ''.join(new_file_array)

        return new_file

        
    def base64_to_string(self, s):
        try:
            return base64.b64decode(s).decode('utf-8')
        except:
            return None
            
    def convert_cipher_to_fallback(self, s_line, cipher_key):
        return s_line.replace(cipher_key, 'data-ciphers')
    
    def is_layer_of_vpn_connection(self, s_line, layer_key):
        return s_line[:3] == layer_key
    
    def is_cipher(self, s_line, cipher_key):
         return s_line[:6] == cipher_key
     
    # Main runner 
    def scrape_ovpn_files(self, number_of_files): 
        ovpn_files = []
        
        html_text = BeautifulSoup(self.page.content, 'html.parser').get_text()
        separated_text = re.split(',,|\n', html_text)
        
        for row in separated_text:
            file_in_string_format = self.base64_to_string(row.strip())

            if file_in_string_format is not None:
                # The client needs some additional configs in the .ovpn file to work
                ovpn_file = self.append_additional_required_vpn_configurations(file_in_string_format)

                ovpn_files.append(ovpn_file)

                if len(ovpn_files) >= number_of_files: return ovpn_files