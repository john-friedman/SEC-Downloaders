from sec_downloaders import SEC_Downloader
from sec_parsers import Filing


# Set up the SEC downloader
downloader = SEC_Downloader()
downloader.set_headers("John Doe", "johndoe@example.com")

df = downloader.basic_company_data

# Download the data
url = 'https://www.sec.gov/Archives/edgar/data/320193/000119312514383437/d783162d10k.htm'
download = downloader.download(url)

filing = Filing(download)
filing.parse()
filing.save_xml('test.xml')