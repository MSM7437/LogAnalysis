import os
import re
from datetime import datetime, timedelta, timezone
import urllib.request

# URL of the log file
url = "https://s3.amazonaws.com/tcmg476/http_access_log"

# Local cache file path
local_cache_file = "http_access_log.txt"

def is_cache_outdated(cache_file):
    if not os.path.exists(cache_file):
        return True
    last_modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
    current_time = datetime.now()
    return (current_time - last_modified_time) > timedelta(hours=24)

if not os.path.exists(local_cache_file) or is_cache_outdated(local_cache_file):
    urllib.request.urlretrieve(url, local_cache_file)

log_entry_pattern = r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} -\d{4})\]'

utc_timezone = timezone.utc

start_date = datetime(1995, 10, 11, tzinfo=utc_timezone)

six_months_ago = start_date - timedelta(days=180)

total_requests = 0

with open(local_cache_file, 'r') as log_file:
    for line in log_file:
        match = re.search(log_entry_pattern, line)
        if match:
            log_date = datetime.strptime(match.group(1), '%d/%b/%Y:%H:%M:%S %z')
            if log_date >= six_months_ago:
                total_requests += 1

print(f"Total requests in the past 6 months: {total_requests}")

