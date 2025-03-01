import requests
from urllib.parse import urlparse

def check_robot_txt(url):
    # Parse the URL to ensure it is properly formatted
    parsed_url = urlparse(url)
    
    # If no domain is provided, return error message
    if not parsed_url.netloc:
        print("Invalid URL")
        return
    
    # Construct the URL for robots.txt (standard location for robots.txt)
    robots_url = parsed_url.scheme + "://" + parsed_url.netloc + "/robots.txt"
    
    try:
        # Make an HTTP GET request to the robots.txt URL
        response = requests.get(robots_url)
        
        # Check if robots.txt exists
        if response.status_code == 200:
            print(f"robots.txt found at {robots_url}:")
            print(response.text)
        else:
            print(f"No robots.txt found at {robots_url}.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error checking robots.txt: {e}")

if __name__ == "__main__":
    url = input("Enter the website URL to check for robots.txt: ")
    check_robot_txt(url)
