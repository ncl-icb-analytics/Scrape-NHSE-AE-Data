# Scrape NHSE A&E Data

This project contains a Python script to scrape publicly available A&E attendance and emergency admission data from the NHS England website. The script downloads CSV files for specified years, combines them into a single dataset, and saves the output.

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
  - `ncl_ae_data.csv`: Contains filtered data for NCL trusts.

## Column Headers

The combined CSV files will have the following columns:
  - Period
  - Org Code
  - Parent Org
  - Org name
  - A&E attendances Type 1
  - A&E attendances Type 2
  - A&E attendances Other A&E Department
  - A&E attendances Booked Appointments Type 1
  - A&E attendances Booked Appointments Type 2
  - A&E attendances Booked Appointments Other Department
  - Attendances over 4hrs Type 1
  - Attendances over 4hrs Type 2
  - Attendances over 4hrs Other Department
  - Attendances over 4hrs Booked Appointments Type 1
  - Attendances over 4hrs Booked Appointments Type 2
  - Attendances over 4hrs Booked Appointments Other Department
  - Patients who have waited 4-12 hs from DTA to admission
  - Patients who have waited 12+ hrs from DTA to admission
  - Emergency admissions via A&E - Type 1
  - Emergency admissions via A&E - Type 2
  - Emergency admissions via A&E - Other A&E department
  - Other emergency admissions

## License

This repository is dual licensed under the Open Government v3 & MIT. All code and outputs are subject to Crown Copyright.
