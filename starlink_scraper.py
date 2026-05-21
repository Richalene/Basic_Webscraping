import json
import pandas as pd
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to chrome instance with remote debugging enabled
options = Options()
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

driver = webdriver.Chrome(options=options)
print(f"Connected to: {driver.current_url}")

# Fetch data
raw_data = driver.execute_async_script("""
    const callback = arguments[arguments.length - 1];
    fetch('https://starlink.com/api/telemetryagg/v1/data-usage/account/ACC-2735603-74738-20/service-line/AST-2293597-46342-54/annotated', {
        credentials: 'include'
    })
    .then(r => r.json())
    .then(data => callback(data))
    .catch(err => callback({error: err.toString()}));
""")

if 'error' in raw_data:
    print(f"Fetch failed: {raw_data['error']}")
    driver.quit()
    exit()
else:
    print("Data fetched successfully")
    print(f"Keys: {list(raw_data.keys())}")

# Save raw JSON locally as backup
with open('data/starlink_data.json', 'w') as f:
    json.dump(raw_data, f, indent=2)
print("Raw JSON saved to data/starlink_data.json")

# Parse billing cycles into a DataFrame
billing_cycles = raw_data['content']['billingCyclesAnnotated']
now = datetime.now(timezone.utc).replace(tzinfo=None)
rows = []

for cycle in billing_cycles:
    start_date = pd.to_datetime(cycle['startDate'].split('T')[0])
    for i, usage_array in enumerate(cycle['dailyData']):
        if not usage_array:
            continue
        date = start_date + pd.Timedelta(days=i)
        if date > now:
            continue
        rows.append({'date': date, 'usage_gb': round(usage_array[0], 2)})

df = pd.DataFrame(rows)
df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.day_name()
df['week'] = df['date'].dt.strftime('%G-W%V')
df['month'] = df['date'].dt.strftime('%Y-%m')

print(f"Processed {len(df)} days of data")

# Overall stats
stats = df['usage_gb'].agg(['count', 'sum', 'mean']).round(2)
stats.index = ['Total Days', 'Total GB', 'Avg Daily GB']
print("\nOverall Statistics:")
print(stats)

# Top 5 highest usage days
top_days = df.nlargest(5, 'usage_gb')
print("\nTop 5 Highest Usage Days:")
print(top_days[['date', 'day_of_week', 'usage_gb']])

# Average usage by day of week
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_avg = df.groupby('day_of_week')['usage_gb'].mean().round(2).reindex(dow_order)
print("\nAverage Usage by Day of Week:")
print(dow_avg)

# Weekly and monthly summaries
weekly = df.groupby('week')['usage_gb'].sum().round(2).reset_index()
weekly.columns = ['week', 'total_gb']

monthly = df.groupby('month')['usage_gb'].agg(
    total_gb='sum',
    average_daily_gb='mean',
    max_daily_gb='max',
    min_daily_gb='min',
    days_count='count'
).round(2).reset_index()

print("\nWeekly Summary:")
print(weekly)
print("\nMonthly Summary:")
print(monthly)

# Export CSVs
df[['date', 'day_of_week', 'week', 'month', 'usage_gb']].to_csv('data/starlink_daily_usage.csv', index=False)
weekly.to_csv('data/starlink_weekly_summary.csv', index=False)
monthly.to_csv('data/starlink_monthly_summary.csv', index=False)
print("\nCSVs saved to /data folder")

# Write report
with open('data/starlink_usage_report.txt', 'w', encoding='utf-8') as f:
    f.write('=' * 60 + '\n')
    f.write('STARLINK DATA USAGE ANALYSIS REPORT\n')
    f.write('=' * 60 + '\n\n')

    f.write('OVERALL STATISTICS\n')
    f.write('-' * 30 + '\n')
    for label, val in stats.items():
        f.write(f"{label:<20}: {val}\n")

    f.write('\nTOP 5 HIGHEST USAGE DAYS\n')
    f.write('-' * 30 + '\n')
    for i, (_, row) in enumerate(top_days.iterrows(), 1):
        f.write(f"{i}. {row['date'].strftime('%Y-%m-%d')} ({row['day_of_week']}): {row['usage_gb']} GB\n")

    f.write('\nAVERAGE USAGE BY DAY OF WEEK\n')
    f.write('-' * 30 + '\n')
    for day, avg in dow_avg.items():
        f.write(f"{day:<10}: {avg} GB\n")

    f.write('\n' + '=' * 60 + '\n')
    f.write('MONTHLY DATA USAGE REPORT\n')
    f.write('=' * 60 + '\n')
    for _, row in monthly.iterrows():
        f.write(f"\n{row['month']}\n")
        f.write(f"  Total Usage:    {row['total_gb']} GB\n")
        f.write(f"  Daily Average:  {row['average_daily_gb']} GB\n")
        f.write(f"  Peak Day:       {row['max_daily_gb']} GB\n")
        f.write(f"  Lowest Day:     {row['min_daily_gb']} GB\n")
        f.write(f"  Days Recorded:  {int(row['days_count'])}\n")

    f.write('\n' + '=' * 60 + '\n')
    f.write(f"Grand Total: {monthly['total_gb'].sum().round(2)} GB across {len(monthly)} months\n")
    f.write('\n' + '=' * 60 + '\n')
    f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print("Report saved: data/starlink_usage_report.txt")

# Export raw data as CSV
raw_df = pd.DataFrame([{
    'date': pd.to_datetime(cycle['startDate'].split('T')[0]) + pd.Timedelta(days=i),
    'usage_gb': usage_array[0] if usage_array else None
} for cycle in billing_cycles
  for i, usage_array in enumerate(cycle['dailyData'])
  if usage_array], columns=['date', 'usage_gb'])

raw_df.to_csv('data/starlink_raw_export.csv', index=False)
print(f"Raw data exported: {len(raw_df)} records to data/starlink_raw_export.csv")

# Close browser connection
driver.quit()
print("\nBrowser connection closed.")