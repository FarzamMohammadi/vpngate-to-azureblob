import requests
from bs4 import BeautifulSoup
import csv
import os.path
from itertools import islice
import pathlib

class Scraper:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        soup = BeautifulSoup(self.page.content, "html.parser")
        reader = csv.reader(soup.get_text(separator='\n\n'))
        # print(soup.get_text(separator='\n'))
        for row in reader:
            print(row)
            # openvpn_base64file = row[14]
            # filepath = pathlib.Path(__file__).parent.resolve() + '/' + index
            # print(filepath)
            # with open(filepath, "wb") as fh:
            #     fh.write(openvpn_base64file.decode('base64'))

            # print(data)     
        # table = soup.find('table', id="vg_hosts_table_id")
        # print(table)

#15