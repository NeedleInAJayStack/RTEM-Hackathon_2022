# RTEM Hackathon 2022

This repository contains Jay Herron's code for submission to the RTEM Hackathon 2022.

## Getting Started

1. Clone this repo: `git clone <address_of_this_repo>`
2. Install python dependencies: `pip install -r requirements.txt`
3. The API key to use is detected from the `API_KEY` environment variable. Either set this variable or add a `.env` file to the root directory and set the variable there.

## Datasets

- kpis.csv: The KPI results for each building across their entire running operation. result of running `process.py` across the dataset.
- electrical_consumption.csv: Filtered for "Electrical Consumption" point type on equipment of "meter", "site", "panel", or "virtual". Then hand-picked the ones that appeared to be total site energy consumption
