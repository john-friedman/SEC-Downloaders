import re
import requests
import warnings
import pandas as pd
from importlib import resources
from pathlib import Path


def extract_cik_and_accession(url):
    # Regular expression pattern to match CIK and accession number
    pattern = r"/data/(\d+)/(\d+)/"
    
    # Search for the pattern in the URL
    match = re.search(pattern, url)
    
    if match:
        cik = match.group(1)
        accession_number = match.group(2)
        return int(cik), int(accession_number) # To drop leading zeros
    else:
        return None, None
    

class SEC_Download:
    def __init__(self, html, metadata):
        self.metadata = metadata
        self._html = html
        self._parsed_html = None

    def __str__(self):
        return self._html

    def __getitem__(self, key):
        return self._html[key]

    def find(self, *args, **kwargs):
        return self._html.find(*args, **kwargs)

    @property
    def html(self):
        if self._parsed_html is None:
            self._parsed_html = setup_html(self._html)
        return self._parsed_html
    
    
class SEC_Downloader:
    def __init__(self):
        self.headers = {}
        self.content = None
        self.metadata = {}

        self.basic_company_data = None
        self.load_basic_company_data()

    def load_basic_company_data(self):
        package_dir = Path(__file__).resolve().parent.parent
        data_file = package_dir / 'data' / 'basic_company_data.csv'
        self.basic_company_data = pd.read_csv(data_file)

    def _metadata_from_url(self, url):
        # Extract CIK and accession number from the URL
        cik, accession_number = extract_cik_and_accession(url)
        
        # Create initial metadata dictionary
        metadata = {
            'cik': cik,
            'accession_number': accession_number,
            'url': url
        }
        
        # Filter the basic company data for the matching CIK
        company_data = self.basic_company_data[self.basic_company_data['cik'] == cik]
        
        if not company_data.empty:
            # If a match is found, update metadata with company data
            metadata.update(company_data.iloc[0].to_dict())
        
        return metadata
    def download(self,url):
        # nudge to set your own headers
        if self.headers is None:
            raise ValueError("Error: Please set your own headers using set_headers(name, email).")

        sec_response = requests.get(url, headers=self.headers)
        
        if sec_response.status_code != 200:
            print(f"Error {sec_response.status_code}: failed to download {self.url}")
            return

        # important to encode the text as utf-8 as the lxml parser expects it
        html = sec_response.text.encode("utf-8").decode("utf-8")
        metadata = self._metadata_from_url(url)

        download = SEC_Download(html, metadata)
        return download

    def set_headers(self, name, email):
        self.headers['User-Agent'] = f"{name} {email}"

    def __str__(self):
        return self.content if self.content else "No content downloaded"

    def __repr__(self):
        return f"SEC_Download(url='{self.url}')"