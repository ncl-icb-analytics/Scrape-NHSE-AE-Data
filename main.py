import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import calendar

# Constants
BASE_URL = 'https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/'
START_YEAR = 2021
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
NCL_ORG_CODES = ["RP6", "RAP", "RAL", "RAN", "RKE", "RRV"]

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Functions
def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_valid_years(start_year):
    current_year = datetime.now().year
    valid_years = [f"{year}-{str(year + 1)[-2:]}" for year in range(start_year, current_year + 1)]
    return valid_years

def get_yearly_links(base_url, valid_years):
    links = []
    for year in valid_years:
        possible_urls = [
            f"{base_url}ae-attendances-and-emergency-admissions-{year}/"
        ]
        for url in possible_urls:
            if url_exists(url):
                links.append(url)
                break
    return links

def url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

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

def parse_period_to_date(period_str):
    try:
        if pd.isna(period_str) or 'TOTAL' in period_str.upper():
            return None
        _, month, year = period_str.split('-')
        month_number = datetime.strptime(month, "%B").month
        last_day = calendar.monthrange(int(year), month_number)[1]
        return datetime(int(year), month_number, last_day)
    except Exception as e:
        print(f"Failed to parse date from period: {period_str} - {e}")
        return None

def combine_csvs(data_dir, national_output_file, ncl_output_file, ncl_org_codes):
    all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not all_files:
        print("No CSV files to combine.")
        return
    
    combined_df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

    # Convert Period to date and sort dataframe
    combined_df['Period'] = combined_df['Period'].apply(parse_period_to_date)
    combined_df = combined_df.dropna(subset=['Period']).sort_values(by='Period', ascending=False)

    combined_df.to_csv(national_output_file, index=False)
    
    ncl_df = combined_df[combined_df['Org Code'].isin(ncl_org_codes)]
    ncl_df.to_csv(ncl_output_file, index=False)

def main():
    valid_years = get_valid_years(START_YEAR)
    yearly_links = get_yearly_links(BASE_URL, valid_years)
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
    
    national_output_file = os.path.join(OUTPUT_DIR, 'national_ae_data.csv')
    ncl_output_file = os.path.join(OUTPUT_DIR, 'ncl_ae_data.csv')
    combine_csvs(DATA_DIR, national_output_file, ncl_output_file, NCL_ORG_CODES)
    
    print(f"National combined CSV saved to {national_output_file}")
    print(f"NCL combined CSV saved to {ncl_output_file}")

# Run the script
if __name__ == "__main__":
    main()
