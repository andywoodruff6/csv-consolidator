"""
Usage:
    uv run main.py
"""
from modules.csv import check_weekly_file_exists, update_weekly_tracker
from modules.chart import generate_line_chart

def main():
    # Check and create weekly tracker file if it doesn't exist
    if check_weekly_file_exists():
        print("Weekly tracker file is ready.")
    
    # Update the weekly tracker with new export data
    update_weekly_tracker()
    print("Weekly tracker has been updated with new export data.")
    
    # Generate the line chart
    generate_line_chart()
    print("Line chart has been generated.")
    
    print("🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡")

if __name__ == "__main__":
    main()
