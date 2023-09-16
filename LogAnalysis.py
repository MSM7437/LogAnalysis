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

total_requests = 0

with open(local_file, 'r') as log_file:
    for line in log_file:
        match = re.search(log_entry_pattern, line)
        if match:
            log_date = datetime.strptime(match.group(1), '%d/%b/%Y:%H:%M:%S %z')
            if log_date >= six_months_ago:
                total_requests += 1

print(f"The total number of requests in the past 6 months: {total_requests}")

#Total number of request
with open(local_file , 'r') as file:
    li = file.readlines()
total_log = len(li)
print(f"The total number of requests found in the log: {total_log}")

# Percent of unsuccessful or redirected logs
def calculate_percentage_not_successful(log_file_path):
    not_successful_count = 0
    total_requests = 0

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            total_requests += 1
            status_code_match = re.search(r'\s(\d{3})\s', line)
            if status_code_match:
                status_code = int(status_code_match.group(1))
                if 400 <= status_code < 500:
                    not_successful_count += 1

    if total_requests > 0:
        percentage_not_successful = (not_successful_count / total_requests) * 100
    else:
        percentage_not_successful = 0.0

    return percentage_not_successful

def calculate_percentage_redirected(log_file_path):
    redirected_count = 0
    total_requests = 0

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            total_requests += 1
            status_code_match = re.search(r'\s(\d{3})\s', line)
            if status_code_match:
                status_code = int(status_code_match.group(1))
                if 300 <= status_code < 400:
                    redirected_count += 1

    if total_requests > 0:
        percentage_redirected = (redirected_count / total_requests) * 100
    else:
        percentage_redirected = 0.0

    return percentage_redirected

percentage_not_successful = calculate_percentage_not_successful(local_file)
percentage_redirected = calculate_percentage_redirected(local_file)

print(f"What percentage of the requests were not successful (4xx codes): {percentage_not_successful:.2f}%")
print(f"What percentage of the requests were redirected elsewhere (3xx codes): {percentage_redirected:.2f}%")

