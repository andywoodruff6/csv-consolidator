import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import datetime

def generate_line_chart():
    """
    Generates a multi-line chart from 'weekly_csv_timelines_tracker.csv' with:
    - X-axis: Date
    - Y-axis: Multiple metrics
    - Title: 'Weekly Timelines Tracker'
    Saves the chart as '{year}-{week}.png' in '~/SynologyDrive/weekly_review'.
    """
    tracker_path = Path.home() / 'SynologyDrive' / 'weekly_review' / 'weekly_csv_timelines_tracker.csv'
    
    if not tracker_path.exists():
        print(f"Error: CSV file not found at {tracker_path}")
        return
        
    df = pd.read_csv(tracker_path)
    # print(f"Loaded DataFrame shape: {df.shape}")
    # print("DataFrame head:\n", df.head())
    
    # Convert 'Date' column to datetime if not already
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter data for the last 4 weeks ending with today's date
    end_date = df['Date'].max()
    start_date = end_date - pd.Timedelta(weeks=4)
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    # print(f"Filtered DataFrame shape: {df_filtered.shape}")
    # print("Filtered DataFrame head:\n", df_filtered.head())
    
    if df_filtered.empty:
        print("Error: No data available for plotting after filtering")
        return
    
    # Plotting
    plt.figure(figsize=(12, 7))
    
    # Get all numeric columns that contain 'total' in their name
    metrics = [col for col in df_filtered.select_dtypes(include=['int64', 'float64']).columns if 'total' in col.lower()]
    # print("Plotting total metrics:", metrics)
    
    for metric in metrics:
        sns.lineplot(data=df_filtered, x='Date', y=metric, marker='o', label=metric.replace(' total', ''))
    
    plt.title('Weekly Timelines Tracker')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the chart to both locations
    save_chart(plt)
    plt.close()

def save_chart(plt):
    """
    Save the chart to multiple locations with the filename format: '{year}-{week}.png'
    """
    current_week = datetime.date.today().isocalendar()[1]
    current_year = datetime.date.today().year
    filename = f'{current_year}-{current_week}.png'
    
    # Save locations
    save_paths = [
        Path.home() / 'SynologyDrive' / 'weekly_review' / filename,
        Path.home() / 'Documents' / 'My Second Brain' / '5 Assets' / filename
    ]
    
    for save_path in save_paths:
        # Create directory if it doesn't exist
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
        print(f"Saved chart to: {save_path}")
