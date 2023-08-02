import os
import re
import json
import socket
import urllib3
import requests
import subprocess
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# py to compile program into binary

# Check if there is an update for the requests package
def check_package_update():
    print("Verifying requests module is present for python3...")
    sleep(0.5)
    try:
        os.system("python3 -m pip install requests")
    except Exception as e:
        print(f"Error checking for updates for requests. Error message: {e}")

check_package_update()

# Constants
ip_address = socket.gethostbyname(socket.gethostname())
TASKS = [
  {"name": "User Management", "method": "GET", "url": f"https://{ip_address}/api/system/about", "expected_regex": r"releaase_name"},
  # {"name": "Management", "method": "GET", "url": f"https://{ip_address}/endpoint_2", "expected_regex": r"Expected Regex Pattern 2"}
  # Add more tasks here
]

# Validate Key Input
def keyValidation():
    # b653e7c6-434c-4829-9b0c-518c45e876dd
    key_regex = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"

    user_input = input("Please enter the Security Key Generated: ")

    # Validate Key Format is correct
    while not re.match(key_regex, user_input):
        print("Incorrect Input Format...")
        sleep(0.5)
        user_input = input("Please enter the Security Key Generated: ")

    print("Security Key entered: ", user_input)
    print("Validating SEC KEY Works. One second please...")
    sleep(1.0)

    # Validation
    header = {
    'SEC': user_input,
    }

    url = f"https://{ip_address}/api/system/about"

    response = requests.get(url, headers=header, verify=False)

    if response.ok:
        print("Security Key valid...\n")
    else:
        print(f"Invalid Security Key. Regenerate Key and try again...")
        exit()

    return user_input

# Create an encrypted file for submission
def results():
    return

# Main function
def main():
    print("\n\nSuper cool QRadar 150 validation script by Brandon Gonzalez")

    # Receive SEC_KEY and Validate the SEC_KEY works
    SEC_KEY = keyValidation()
    
    # Header for GET requests on tasks
    header = {
    'SEC':SEC_KEY,
    }

    # Loop through tasks and print results
    for task in TASKS:
        url = task["url"]
        method = task["method"]
        
        if method == "GET":
            response = requests.get(url, headers=header, verify=False)

        if response.ok:
            actual_response = json.dumps(response.text)
            expected_regex = task["expected_regex"]
            match = re.search(expected_regex, actual_response)
            
            if match:
                print(f"{task['name']}: Pass")
            else:
                print(f"{task['name']}: Fail")
        else:
            print(f"{task['name']}: Invalid Response Code")

    # do while for input validation asking to create the file
    while True:
        choice = input("\nWould you like to save your results?\ny or n: ")
        if choice == 'y':
            results()
            break
        elif choice == 'n':
            break
        else:
            print("Invalid Option...")
            sleep(0.5)

if __name__ == '__main__':
    main()
