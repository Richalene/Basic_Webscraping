# BASIC STARLINK WEB SCRAPER
 
Extracts daily data usage from a Starlink account page using Selenium and exports it to CSV with data analysis using pandas.
 
---
 
## Requirements
 
- Python 3.8+
- Google Chrome
- ChromeDriver (matching your Chrome version)
- Dependencies listed in `requirements.txt`
Install dependencies:
 
```bash
pip install -r requirements.txt
```
 ---
 
## requirements.txt
 
```
pandas
jupyter
selenium
```
 
---
 
## Usage
 
### 1. Launch Chrome with remote debugging
 
Open a terminal and type:
 
```bash
start chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\chrome-debug
```
 
### 2. Log in to Starlink
 
In that Chrome window, go to [starlink.com](https://starlink.com) and log in to your account. Once logged in go into My Subscriptions.
 
### 3. Run the notebook
 
```bash
jupyter notebook starlink_scraper.ipynb
```
 
Execute all cells in order. When prompted, confirm the browser is on the correct page before continuing.
 
---
 
## How it works
 
The notebook attaches to the open Chrome session via remote debugging and calls the Starlink internal API endpoint directly using the browser's authenticated cookies — no password handling in code.
 
```
Chrome (logged in) → Selenium attaches → JS fetch to API → JSON → pandas → CSV + report
```
 
---
 
## Output Files
 
| File | Description |
|------|-------------|
| `starlink_data.json` | Raw API response saved as backup |
| `starlink_daily_usage.csv` | Daily usage with date, day of week, week, and month |
| `starlink_weekly_summary.csv` | Total GB per week |
| `starlink_monthly_summary.csv` | Monthly totals, averages, min/max |
| `starlink_usage_report.txt` | Full analysis report |
| `starlink_raw_export.txt` | Raw data|
 
---
 

 
## Output Format
 
`starlink_daily_usage.csv` sample:
 
| date | day_of_week | week | month | usage_gb |
|------|-------------|------|-------|----------|
| 2025-11-17 | Monday | 2025-W47 | 2025-11 | 17.49 |
| 2025-11-18 | Tuesday | 2025-W47 | 2025-11 | 13.31 |
 

---
 
## Notes
 
- ChromeDriver version must match your installed Chrome version — download from [chromedriver.chromium.org](https://chromedriver.chromium.org).
