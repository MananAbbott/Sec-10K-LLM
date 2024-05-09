from sec_edgar_downloader import Downloader
import sys, os
#Download SEC 10-K filings for given companies between start_year and end_year.
def download_10k_filings(companies, start_year, end_year, save_path, email_address):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    dl = Downloader(save_path, email_address)
    for company in companies:
        for year in range(start_year, end_year + 1):
            dl.get("10-K", company, after=f"{year}-01-01", before=f"{year}-12-31")

    print("Download completed.")


companies = ["AAPL", "MSFT", "GOOGL"]
start_year = 1995
end_year = 2023
save_path = "data"
email_address = 'mhabbott@umass.edu'

download_10k_filings(companies, start_year, end_year, save_path, email_address)

