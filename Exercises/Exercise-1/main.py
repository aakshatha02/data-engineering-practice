import requests
import os
import zipfile
from urllib.parse import urlparse

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

download_dir = 'downloads'

def create_download_dir():
    os.makedirs(download_dir, exist_ok=True)

def get_filename_from_url(url):
    return os.path.basename(urlparse(url).path)

def download_file(url):
    try:
        response = requests.get(url, stream=True, timeout=10)

        if response.status_code != 200:
            print(f'Failed to download: {url}')
            return None
        filename = get_filename_from_url(url)
        filepath = os.path.join(download_dir, filename)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded: {filename}")
        return filepath
    
    except requests.RequestException as e:
        print(f"Error downloading {url}:{e}")
        return None
    
def unzip_and_cleanup(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
        os.remove(zip_path)
        print(f"Extracted and removed:{os.path.basename(zip_path)}" )

    except zipfile.BadZipFile:
        print(f"Bad zip file: {zip_path}")
    

def main():
    create_download_dir()

    for url in download_uris:
        zip_path = download_file(url)
        if zip_path:
            unzip_and_cleanup(zip_path)

if __name__ == "__main__":
    main()
