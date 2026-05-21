# Starlink Web Scraper

A Selenium-based tool that extracts daily Starlink usage data from your logged-in account session via Chrome remote debugging, then processes it with pandas and exports basic reports.

---

## Requirements

- Python 3.8+
- Google Chrome (latest recommended)
- ChromeDriver matching your Chrome version — [download here](https://chromedriver.chromium.org)

---

## Usage

Double-click **`run_scraper.bat`**

---

## How It Works

The scraper attaches to an existing Chrome session via Selenium's remote debugging mode. This approach avoids storing credentials in code — you log in manually, and the scraper piggybacks on your live session.

```
Chrome (logged-in session)
        ↓
Selenium attaches via remote debugging
        ↓
Extracts usage data from DOM / session
        ↓
pandas processes the data
        ↓
CSV files + reports exported
```

---

## Project Structure

```
starlink-scraper/
├── starlink_scraper.py        # Main script
├── starlink_scraper.ipynb     # Notebook version
├── run_starlink.bat           # One-click runner (Windows)
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── data/                      # Output files
```

---

## Output Files

| File | Description |
|---|---|
| `starlink_data.json` | Raw extracted data backup |
| `starlink_daily_usage.csv` | Daily usage breakdown |
| `starlink_weekly_summary.csv` | Weekly totals |
| `starlink_monthly_summary.csv` | Monthly statistics |
| `starlink_usage_report.txt` | Full analysis report |
| `starlink_raw_export.txt` | Raw extracted text |

### Sample — `starlink_daily_usage.csv`

| date | day_of_week | week | month | usage_gb |
|---|---|---|---|---|
| 2025-11-17 | Monday | 2025-W47 | 2025-11 | 17.49 |
| 2025-11-18 | Tuesday | 2025-W47 | 2025-11 | 13.31 |

---

## Notes

- **ChromeDriver version must match your Chrome version.** Mismatches will cause the scraper to fail.
- **Do not close the Chrome debugging window** while the scraper is running.
- **Log in before running the script.** The scraper relies on your active session and has no credential handling of its own.
