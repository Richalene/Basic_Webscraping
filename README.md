# Starlink

Extracts daily data usage from a Starlink account page and exports it to CSV using Python and pandas.

---

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Clone the repo:

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Place your `starlink_data.json` file in the root directory (exported from the Starlink usage page).

3. Run the notebook:

```bash
jupyter notebook starlink_analysis.ipynb
```

4. Execute all cells. The following output files will be generated:

| File | Description |
|------|-------------|
| `starlink_daily_usage.csv` | Daily data usage with date, day of week, week, and month |
| `starlink_weekly_summary.csv` | Total GB per week |
| `starlink_monthly_summary.csv` | Monthly totals, averages, min/max |
| `starlink_usage_report.txt` | Full stats report including top 5 usage days |

---

## Output Format

`starlink_daily_usage.csv` sample:

| date | day_of_week | week | month | usage_gb |
|------|-------------|------|-------|----------|
| 2025-11-17 | Monday | 2025-W47 | 2025-11 | 17.49 |
| 2025-11-18 | Tuesday | 2025-W47 | 2025-11 | 13.31 |

---

## Requirements.txt

```
pandas
jupyter
```

---

## Notes

- Zero-usage days (future dates) are automatically excluded from analysis.
- Weekly totals are deduplicated across billing cycle boundaries.
- All timestamps are handled in UTC to avoid timezone offset issues.
