import os
import re
from datetime import datetime, timedelta, timezone
import urllib.request


# URL of the log file
url = "https://s3.amazonaws.com/tcmg476/http_access_log"

# Local cache file path
local_file = "downloaded_log_file.log"

if os.path.exists(local_file):
    print(f"The file '{local_file}' already exists. Performing Analysis, please wait...")
else:
    try:
        # Open the URL and read its content
        with urllib.request.urlopen(url) as response:
            # Check if the HTTP response status code is 200 (OK)
            if response.status == 200:
                # Open a local file for writing the log data in binary mode ('wb')
                with open('downloaded_log_file.log', 'wb') as file:
                    # Read the content from the response and write it to the local file
                    file.write(response.read())
                print("Log file downloaded successfully. Performing Calculations, please wait...")
            else:
                # If the status code is not 200, print an error message
                print(f"Log file failed to download. Status code: {response.status}")
    except Exception as e:
        # Handle any exceptions that may occur during the process
        print(f"An error occurred: {str(e)}")

#6 months of entries
log_entry_pattern = r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})\]'

utc_timezone = timezone.utc

start_date = datetime(1995, 10, 11, tzinfo=utc_timezone)

six_months_ago = start_date - timedelta(days=180)

six_month_total = 0

#Total number of request
with open(local_file , 'r') as file:
    li = file.readlines()
total_log = len(li)
print(f"The total number of requests found in the log: {total_log}")

# Monthly files & 6 months of log
log_folder = "monthly_logs"
os.makedirs(log_folder, exist_ok=True)

log_files_by_month = {}

def get_month_year_key(log_date):
    return log_date.strftime("%Y_%m")

# Log separated by month so marketing can analyze each monthly period, (13 different files/month)
with open(local_file, 'r') as log_file:
    for line in log_file:
        match = re.search(log_entry_pattern, line)
        if match:
            log_date = datetime.strptime(match.group(1), '%d/%b/%Y:%H:%M:%S %z')
            if log_date >= six_months_ago:
                six_month_total += 1

            month_year_key = get_month_year_key(log_date)

            if month_year_key not in log_files_by_month:
                log_file_path = os.path.join(log_folder, f"log_{month_year_key}.log")
                log_files_by_month[month_year_key] = open(log_file_path, 'a')

            log_files_by_month[month_year_key].write(line)

print(f"The total number of requests in the past 6 months: {six_month_total}")

for log_file in log_files_by_month.values():
    log_file.close()

# Number of requests made each day, each week on average, and each month on average
average_daily = 0
average_weekly = 0
average_monthly = 0

log_time_days = 353
log_time_weeks = (353 / 7)
log_time_months = (353 / 30)

average_daily = total_log // log_time_days
average_weekly =  total_log // log_time_weeks
average_monthly = total_log // log_time_months

print(f"The average number of requests per day: {average_daily}")
print(f"The average number of requests per week: {average_weekly}")
print(f"The average number of requests per month: {average_monthly}")

# Percent of unsuccessful or redirected logs
def percentage_of_status_code(log_file_path, start_code, end_code):
    count = 0
    total_requests = 0

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            total_requests += 1
            status_code_match = re.search(r'\s(\d{3})\s', line)
            if status_code_match:
                status_code = int(status_code_match.group(1))
                if start_code <= status_code < end_code:
                    count += 1

    if total_requests > 0:
        percentage = (count / total_requests) * 100
    else:
        percentage = 0.0

    return percentage

percentage_not_successful = percentage_of_status_code(local_file, 400, 500)
percentage_redirected = percentage_of_status_code(local_file, 300, 400)

print(f"Percentage of the requests that were not successful (4xx codes): {percentage_not_successful:.2f}%")
print(f"Percentage of the requests that were redirected elsewhere (3xx codes): {percentage_redirected:.2f}%")
