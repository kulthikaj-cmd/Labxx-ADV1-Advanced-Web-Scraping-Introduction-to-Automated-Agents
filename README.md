# Advanced Web Scraping & Introduction to Automated Agents

This student project demonstrates a configuration-driven web scraper using Selenium. It reads website selectors from a JSON configuration, collects product names and prices across a limited number of pages, and saves structured results to JSON.

## Features

- Uses Selenium to load pages in Chrome.
- Reads scraping rules from `configs/example_site_config.json`.
- Extracts product name, price, product URL, and image URL.
- Supports a configurable page limit and delay.
- Handles missing elements and saves results to `data/scraped_products.json`.

## Project structure

```text
agentic-web-scraper/
├── src/
│   ├── __init__.py
│   ├── driver_manager.py
│   ├── config_parser.py
│   ├── data_models.py
│   ├── utils.py
│   └── scraper_agent.py
├── configs/
│   └── example_site_config.json
├── data/
├── docs/
│   └── ETHICS.md
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- Google Chrome installed
- Internet connection for the first WebDriver setup and scraping

## Install and run on Windows

Open the project folder in VS Code. Select **Terminal → New Terminal**, then run:

```powershell
python -m pip install -r requirements.txt
python main.py
```

`webdriver-manager` downloads a compatible ChromeDriver when needed. The browser runs in headless mode, so its window will not appear. The terminal shows progress and a summary.

The output file is `data/scraped_products.json`.

## Configuration

Edit `configs/example_site_config.json` to change the start URL, CSS selectors, page limit, and output filename. The example uses the educational practice site `books.toscrape.com`.

## Ethics

Only scrape sites where automated access is permitted. Review `robots.txt` and the site's Terms of Service, keep request rates low, and do not republish copyrighted or personal data without permission. This project is for learning purposes.
