import urllib.request  # Import the urllib.request module for making HTTP requests.

# Replace 'your_url_here' with the actual URL of the log file you want to download
url = 'https://s3.amazonaws.com/tcmg476/http_access_log'  # Set the URL of the log file to download.

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

