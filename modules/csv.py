import os
from pathlib import Path
import pandas as pd
from typing import Optional

def check_weekly_file_exists() -> bool:
    """
    Check if 'weekly_csv_timelines_tracker.csv' exists in '~/SynologyDrive/weekly_review'.
    If not, create an empty CSV file in that location.
    Returns True if the file exists or is created successfully.
    """
    file_path = Path.home() / 'SynologyDrive' / 'weekly_review' / 'weekly_csv_timelines_tracker.csv'
    # print(f"[DEBUG] Checking for weekly tracker file at: {file_path}")
    if not file_path.exists():
        # print("[DEBUG] Weekly tracker file not found, creating new one")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Initialize with required columns
        df_empty = pd.DataFrame(columns=['Date', 'Value'])
        df_empty.to_csv(file_path, index=False)
        # print("[DEBUG] Created new empty tracker file")
    return file_path.exists()

def get_new_export() -> Optional[pd.DataFrame]:
    """
    Reads the latest export CSV file from '~/Downloads' matching the pattern 'export_week*_*.csv'.
    Returns a pandas DataFrame if a file is found, otherwise None.
    """
    downloads_path = Path.home() / 'Downloads'
    # print(f"[DEBUG] Searching for export files in: {downloads_path}")
    csv_files = sorted(downloads_path.glob('export_week*_*.csv'), reverse=True)
    # print(f"[DEBUG] Found {len(csv_files)} export files")
    if csv_files:
        # print(f"[DEBUG] Loading newest export file: {csv_files[0]}")
        df = pd.read_csv(csv_files[0])
        # print(f"[DEBUG] Loaded {len(df)} rows from export file")
        # print(f"[DEBUG] Export file columns: {df.columns.tolist()}")
        # Ensure column names match expected format
        if 'date' in df.columns:
            df = df.rename(columns={'date': 'Date'})
        return df
    else:
        # print("[DEBUG] No export files found")
        return None

def convert_cols_to_minutes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert time values in HH:MM format to minutes for all non-date columns.
    """
    df = df.copy()
    for col in df.columns:
        if col != 'Date' and col != 'date':
            try:
                df[col] = df[col].apply(
                    lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if ':' in str(x) else x
                )
            except Exception as e:
                # print(f"[DEBUG] Could not convert column {col}: {e}")
                pass
    return df


def update_tracker(new_export_df: pd.DataFrame, tracker_path: Path) -> None:
    """
    Update the tracker file with new export data, handling totals and sorting.
    Only adds rows with dates that don't already exist in the tracker.
    """
    try:
        tracker_df = pd.read_csv(tracker_path)
        if tracker_df.empty:
            # print("[DEBUG] Tracker file is empty, using only new export data")
            tracker_df = new_export_df
        else:
            # print(f"[DEBUG] Current tracker has {len(tracker_df)} rows")
            # Convert dates to consistent format for comparison
            tracker_df['Date'] = pd.to_datetime(tracker_df['Date'])
            new_export_df['Date'] = pd.to_datetime(new_export_df['Date'])
            
            # Filter out rows with dates that already exist in tracker
            existing_dates = set(tracker_df['Date'].dt.date)
            new_rows = new_export_df[~new_export_df['Date'].dt.date.isin(existing_dates)]
            
            if len(new_rows) > 0:
                # print(f"[DEBUG] Adding {len(new_rows)} new rows")
                tracker_df = pd.concat([tracker_df, new_rows])
            else:
                # print("[DEBUG] No new dates to add")
                pass
            
    except pd.errors.EmptyDataError:
        # print("[DEBUG] Empty tracker file, using only new export data")
        tracker_df = new_export_df

    # print(f"[DEBUG] After merging and deduplication: {len(tracker_df)} rows")
    # print(f"[DEBUG] Combined DataFrame columns: {tracker_df.columns.tolist()}")
    
    date_col = 'Date' if 'Date' in tracker_df.columns else 'date'
    if date_col not in tracker_df.columns:
        print("[ERROR] No 'Date' or 'date' column found in data")
        return
        
    tracker_df.sort_values(by=date_col, ascending=True, inplace=True)
    
    # Save main tracker file
    tracker_df.to_csv(tracker_path, index=False)
    # print("[DEBUG] Saved updated tracker file")
    
    # Save archive copy with timestamp
    archive_dir = Path.home() / 'SynologyDrive' / 'weekly_review' / 'Archive'
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    archive_path = archive_dir / f'weekly_csv_timelines_tracker_{timestamp}.csv'
    tracker_df.to_csv(archive_path, index=False)
    # print(f"[DEBUG] Saved archive copy to: {archive_path}")

def update_weekly_tracker():
    """
    Appends data from the new export file to 'weekly_csv_timelines_tracker.csv' without duplicates.
    Sorts the combined data by date in ascending order and saves the updated CSV.
    """
    tracker_path = Path.home() / 'SynologyDrive' / 'weekly_review' / 'weekly_csv_timelines_tracker.csv'
    # print(f"[DEBUG] Updating tracker at: {tracker_path}")
    
    new_export_df = get_new_export()
    if new_export_df is not None:
        new_export_df = convert_cols_to_minutes(new_export_df)
        update_tracker(new_export_df, tracker_path)
