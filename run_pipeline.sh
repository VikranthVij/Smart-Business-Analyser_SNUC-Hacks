#!/bin/bash

cd /path/to/SmartBusinessAnalyser

source venv/bin/activate

python3 scraper/westside_scraper.py
python3 scraper/westside_detail_scraper.py