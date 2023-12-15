import os
from time import sleep

# py to compile program into binary

# Check if there is an update for the requests package
def check_package_update():
    print("Verifying requests module is present for python3...")
    sleep(0.5)
    try:
        os.system("python3 -m pip install requests")
        os.system("python3 -m pip install urllib3")
    except Exception as e:
        print(f"Error checking for updates for requests. Error message: {e}")

check_package_update()

import re
import json
import socket
import urllib3
import base64
import requests
import subprocess

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Constants
TASKS = [
  {"name": "User Role Management", "qid": "28250072", "regex": r'\[\"\b(SYSTEM.NETWORKHIERARCHY\"[^\s+]+\b)\"\]'}
  # Add more tasks here
]


# Validate Key Input
def keyValidation():
    ip_address = socket.gethostbyname(socket.gethostname())
    
    # b653e7c6-434c-4829-9b0c-518c45e876dd
    key_regex = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"

    print("\nIn order for the script to work, an Authorized Service Token must be made.\nPlease see the following link for more information:\nhttps://www.ibm.com/docs/en/qradar-common?topic=forwarding-creating-authentication-token\n")
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
    print("You have not built that functionality out yet nerd.")
    return

# Main function
def main():
    print("\n\nSuper cool QRadar 150 validation script by Brandon Gonzalez")

    # Receive SEC_KEY and Validate the SEC_KEY works
    SEC_KEY = keyValidation()

    # Code the echo into root.token so the ariel_query script functions

    # Loop through tasks and print results
    for task in TASKS:
        qid = task["qid"]

        out = subprocess.check_output(f'/opt/qradar/bin/ariel_query --query="SELECT payload, * FROM events WHERE qid={qid} LAST 24 HOURS" --output JSON', shell=True)
        decoded = out.decode('ascii')
        dump = json.dumps(decoded)

        # Parse out base64 payload
        regex_exp = r'\bpayload\":\"([^\s+]+\=\=)\"'

        # Use the regex expression to extract the matching string
        match = re.search(regex_exp, decoded)

        # Extract the desired substring from the match object
        if match:
            # Decode the matched string from Base64 to UTF-8
            b64_str = match.group(1)
            utf8_str = base64.b64decode(b64_str).decode('utf-8')

            # Store the resulting string in the desired_output variable
            output = utf8_str
            
            # Compare the output against the tasks regex to verify step completion
            

            #print(f"{task['name']}: Pass")
        else:
            print("Payload match failed: ", task["name"])

        print(output)

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
