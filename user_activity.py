import csv
import os

LOG_FILE = "user_activity.csv"

def log_user_activity(user_id, filename, action):
    """Log user activities like uploads and downloads."""
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, filename, action])

def get_user_activity(user_id):
    """Retrieve user activity from the log file."""
    if not os.path.exists(LOG_FILE):
        return []

    activities = []
    with open(LOG_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                activities.append(row[1:])  # Exclude user_id in response

    return activities
