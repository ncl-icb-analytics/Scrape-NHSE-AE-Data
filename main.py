import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Constants
BASE_URL = 'https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/'
VALID_YEARS = [
    "2024-25", "2023-24", "2022-23", "2021-22", "2020-21",
    "2019-20", "2018-19", "2017-18", "2016-17", "2015-16"
]
DATA_DIR = 'data'
OUTPUT_DIR = 'output'

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_yearly_links(base_url, valid_years):
    links = []
    for year in valid_years:
        url = f"{base_url}ae-attendances-and-emergency-admissions-{year}/"
        links.append(url)
    return links

def get_csv_links(yearly_url):
    html = get_html(yearly_url)
    soup = BeautifulSoup(html, 'html.parser')
    csv_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith('.csv') and a_tag.text.startswith('Monthly A&E'):
            csv_links.append(href)
    return csv_links

def download_csv(url, data_dir):
    response = requests.get(url)
    response.raise_for_status()
    filename = os.path.join(data_dir, os.path.basename(url))
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def combine_csvs(data_dir, output_file):
    all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not all_files:
        print("No CSV files to combine.")
        return
    combined_df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    combined_df.to_csv(output_file, index=False)

def main():
    yearly_links = get_yearly_links(BASE_URL, VALID_YEARS)
    all_csv_links = []

    for yearly_url in yearly_links:
        try:
            csv_links = get_csv_links(yearly_url)
            all_csv_links.extend(csv_links)
        except requests.HTTPError as e:
            print(f"Failed to process {yearly_url}: {e}")

    print(f"Found {len(all_csv_links)} CSV files to download.")

    for csv_link in all_csv_links:
        print(f"Downloading {csv_link}...")
        download_csv(csv_link, DATA_DIR)
    
    output_file = os.path.join(OUTPUT_DIR, 'combined_ae_data.csv')
    combine_csvs(DATA_DIR, output_file)
    print(f"Combined CSV saved to {output_file}")

if __name__ == "__main__":
    main()
