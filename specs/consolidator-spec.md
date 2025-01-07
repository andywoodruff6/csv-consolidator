# CSV Consolidation Spec
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Combine a new csv file with an existing file. Then generate any reports.

## Mid-Level Objective
- Create weekly_csv_timelines_tracker.csv file if not exists
- Copy the data export file into weekly_csv_timelines_tracker.csv
- Generate a line chart with date range of 4 weeks ending with today's date.
- Generate a table png showing status towards the weekly goal.

## Implementation Notes
- No need to import any external libraries beyond existing dependencies
- Comment every new function
- For CLI commands add usage examples starting with `uv run main.py`
- Follow existing code patterns and type safety practices
- Add tests for all new functionality

## Context

### Beginning context
- `main.py`
- `pyproject.toml` (read only)

### Ending context  
- `modules/chart.py`
- `modules/csv.py`
- `modules/output_format.py`

## Low-Level Tasks
> Ordered from start to finish

1. Create files
```aider
CREATE a new file named `modules/chart.py` 
CREATE a new file named `modules/csv.py` 
CREATE a new file named `modules/output_format.py` 
CREATE a new file named `tests/chart.py`
CREATE a new file named `tests/csv.py`
CREATE a new file named `tests/output_format.py`
```
2. Update weekly_csv_timelines_tracker.csv with new data in `modules/csv.py`
```aider
CREATE def check_weekly_file_exists() -> Bool in `modules/csv.py` 
    CREATE weekly_csv_timelines_tracker.csv in ~/SynologyDrive/weekly_review if not exists
CREATE var new_export that reads from ~/Downloads 
    File name examples: export_week1_2025.csv, export_week2_2025.csv, export_week1_2026.csv, etc.
APPEND new_export to weekly_csv_timelines_tracker.csv
    Do Not duplicate rows or columns in weekly_csv_timelines_tracker.csv
    SORT weekly_csv_timelines_tracker.csv by date in ascending order
    SAVE weekly_csv_timelines_tracker.csv
```
3. Generate line chart 
```aider
CREATE def generate_line_chart() in `modules/chart.py`
    CREATE a line chart using matplotlib and seaborn libraries using weekly_csv_timelines_tracker.csv data
        x-axis: Date
        y-axis: Value
        Title: Weekly Timelines Tracker
        Save the chart as {year}-{week}.png in ~/SynologyDrive/weekly_review
```
