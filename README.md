# TLE Scraper

This Python package provides a command line interface to scrape and save TLE (Two Line Element) data for specific satellites, based on their NASA/NORAD catalogue numbers. It also includes functionality to generate an HTML index file for saved TLE data. TLE data contains information about a satellite's orbit.

## Features

* Scrape TLE data from the web using each satellite's catalogue number.
* Save TLE data for individual satellites to a default or specified directory.
* Save TLE data for a batch of satellites.
* Generate an HTML index file for the directory of saved TLE data. Example: https://medaka0213.github.io/TLE-Scaper/

## Commands

1. `python cli.py save <CATNR>` : Saves the two line element (TLE) of a satellite to a file.
2. `python cli.py save_batch <catnr-list>` : A batch process command to save multiple two line elements (TLE) of satellites to a file.
3. `python cli.py gen_html <output-dir>` : Generates an `index.html` file for a directory.

## Environment Variables 

1. `TLE_LIST` : A string of comma-separated catalogue numbers. Default: `"25544, 48274, 20580"`
2. `OUTPUT_DIR` : The directory where TLE data will be saved. Default: `"output"`


## Example Usage

```bash
# Save TLE for a single satellite
python cli.py save 25544

# Save TLE for a batch of satellites
python cli.py save_batch 25544 48274 20580

# Generate index.html for the output directory
python cli.py gen_html
``` 
