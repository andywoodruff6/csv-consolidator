import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import datetime

def generate_bar_chart():
    """
    Generates a bar chart from 'weekly_csv_timelines_tracker.csv' showing:
    - X-axis: Metrics
    - Y-axis: Sum of values for the last week
    - Title: 'Weekly Metrics Summary'
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
    
    # Filter data for the last week
    end_date = df['Date'].max()
    start_date = end_date - pd.Timedelta(weeks=1)
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    if df_filtered.empty:
        print("Error: No data available for plotting after filtering")
        return
    
    # Get all numeric columns except 'Date' and 'all', then calculate their sums
    metrics = [col for col in df_filtered.select_dtypes(include=['int64', 'float64']).columns if col.lower() != 'all']
    sums = df_filtered[metrics].sum()
    
    # Plotting
    plt.figure(figsize=(12, 7))
    
    # Define colors based on values
    colors = ['red' if x < 300 else 'yellow' if x < 500 else 'green' for x in sums.values]
    
    # Create bar chart with colors
    plt.bar(range(len(sums)), sums.values, color=colors)
    plt.xticks(range(len(sums)), sums.index, rotation=45, ha='right')
    
    # Add horizontal line at 600
    plt.axhline(y=600, color='black', linestyle='-', linewidth=1)
    
    plt.title('Weekly Metrics Summary')
    plt.xlabel('Metrics')
    plt.ylabel('Minutes')
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
