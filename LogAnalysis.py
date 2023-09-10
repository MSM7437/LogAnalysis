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
                print("Log file downloaded successfully. Performing analysis, please wait...")
            else:
                # If the status code is not 200, print an error message
                print(f"Failed to download log file. Status code: {response.status}")
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

print(f"Total requests in the past 6 months: {total_requests}")

#Total number of request
with open(local_file , 'r') as file:
    li = file.readlines()
total_log = len(li)
print(f"Number of total requests: {total_log}")
