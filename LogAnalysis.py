import urllib.request  # Import the urllib.request module for making HTTP requests.
import os #module allows interaction with operating system

# Replace 'your_url_here' with the actual URL of the log file you want to download
url = 'https://s3.amazonaws.com/tcmg476/http_access_log'  # Set the URL of the log file to download.
local_file = 'downloaded_log_file.log'

if os.path.exists(local_file):
    print(f"The file '{local_file}' already exists. Download Cancelled.") 

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
                print("Log file downloaded successfully.")
            else:
                # If the status code is not 200, print an error message
                print(f"Failed to download log file. Status code: {response.status}")
    
    except Exception as e:
        # Handle any exceptions that may occur during the process
        print(f"An error occurred: {str(e)}")
    
with open(local_file , 'r') as file:
    li = file.readlines()
total_log = len(li)
print(f"Number of total requests: {total_log}")
