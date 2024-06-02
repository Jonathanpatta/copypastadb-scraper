# Copypasta Database Scraper

## Overview

This project consists of three scripts to scrape copypasta content from [copypastadb.com](https://copypastadb.com).

## Prerequisites

Install the required libraries from `requirements.txt`:

```sh
pip install -r requirements.txt
```

## Instructions

### Step 1: Scrape URLs

Run `scraper.py` to scrape the main page and get the list of URLs from [copypastadb.com/database](https://copypastadb.com/database). This will create `all_href_links.pkl`.

```sh
python scraper.py
```

### Step 2: Scrape Individual URLs

Run `individual_link_scraper.py` to scrape each individual URL and obtain the copypasta content. The content and title are saved every `batch_size` (default is 1000).
You can set the batch_no to start from a particular batch_no after stopping midway.

```sh
python individual_link_scraper.py
```

### Step 3: Convert to CSV

Run `process_to_csv.py` to process all batch files and convert them to a CSV file.

```sh
python process_to_csv.py
```

## Notes

Most of the code was written by Claude with minor tweaks.