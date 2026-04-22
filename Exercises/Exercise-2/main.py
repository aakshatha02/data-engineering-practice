import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
target_timestamp = '2024-01-19 15:27'

download_dir = 'downloads'

def create_dir():
    os.makedirs(download_dir, exist_ok=True)

def find_file():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        if len(cols) < 2:
            continue

        last_modified = cols[1].text.strip()

        if target_timestamp in last_modified:
            link = row.find('a')
            filename = link.get('href')
            return filename
    return None

def download_file(filename):
    file_url = url + filename
    file_path = os.path.join(download_dir, filename)
    
    response = requests.get(file_url, timeout=10)

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'Downloaded: {filename}')
    return file_path

def analyze_file(file_path):
    df = pd.read_csv(file_path)

    df['HourlyDryBulbTemperature'] = pd.to_numeric(df['HourlyDryBulbTemperature'], errors='coerce')
    max_temp = df['HourlyDryBulbTemperature'].max()
    hottest_rows = df[df['HourlyDryBulbTemperature'] == max_temp]
    return hottest_rows

def main():
    create_dir()

    filename = find_file()
    if not filename:
        print('File not found')
        return None
    print(f'Found file: {filename}')

    file_path = download_file(filename)
    result = analyze_file(file_path)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
