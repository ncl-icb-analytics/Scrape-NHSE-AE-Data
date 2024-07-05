# Scrape NHSE A&E Data

This project contains a Python script to scrape A&E attendance and emergency admission data from the NHS England website. The script downloads CSV files for specified years, combines them into a single dataset, and saves the output.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- `requests`
- `beautifulsoup4`
- `pandas`

## Usage

Clone the repository:

```sh
git clone https://github.com/ncl-icb-analytics/Scrape-NHSE-AE-Data
```
```sh
cd Scrape-NHSE-AE-Data
```

Set up a virtual environment:

```sh
python -m venv venv
```
```sh
venv\Scripts\activate
```

Install the dependencies:

```sh
pip install -r requirements.txt
```

Run the script:

```sh
main.py
```

## The script will:

- Scrape the NHS England website for A&E attendance and emergency admission data.
- Downloads all available CSV files.
- Combines the downloaded CSV files into two outputs:
  - `national_ae_data.csv`: Contains all the combined data.
  - `ncl_ae_data.csv`: Contains filtered data for specified local trusts.

## License

This repository is dual licensed under the Open Government v3 & MIT. All code and outputs are subject to Crown Copyright.
