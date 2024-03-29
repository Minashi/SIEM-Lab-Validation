import os
from time import sleep

# py to compile program into binary

# Check if there is an update for the requests package
def check_package_update():
    print("Verifying requests module is present for python3...")
    sleep(0.5)
    try:
        #os.system("python3 -m pip install requests")
        #os.system("python3 -m pip install urllib3")
        #os.system("python3 -m pip install pexpect")
        pass
    except Exception as e:
        print(f"Error checking for updates for requests. Error message: {e}")

check_package_update()

import re
import json
import socket
import urllib3
import base64
import pexpect
import requests
import subprocess

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#----------------------------------------------------------------------------------------------------------------------------
# Constants for labs steps that generate a log
EVENTS = [
    {"name": "User Role Management", "qid": "28250072", "regex": 'Capabilities: { .*(SYSTEM.NETWORKHIERARCHY,SYSTEM.MNGREFERENCEDATA.*Network Overview, Risk Monitoring) }]'},
    {"name": "License Added", "qid": "28250104", "regex": 'License Identity="(keyNFR-ReliaQuest).*",'},
    {"name": "License Allocated", "qid": "28250090", "regex": 'License Identity="(keyNFR-ReliaQuest).*",'},
    #{"name": "EP License Utilization Set", "qid": "", "regex": ''}
    #{"name": "QRadar Assistant Downloaded", "qid": "", "regex": ''}
    {"name": "App Authorized Services", "qid": "28250261", "regex": 'with label QRadar Assistant'},
    {"name": "Assistant XForce Linked", "qid": "28250217", "regex": 'QRadar Assistant.*(\/console\/restapi\/api\/reference_data)'}
  # Add more tasks here
]
#----------------------------------------------------------------------------------------------------------------------------
# For none constant tasks, code here. for example, verifying user exists, etc.
# Constants for labs steps that do not generate a log
INTERNAL = [
    {"name": "User Management", "Location": "/store/configservices/staging/globalconfig/users.conf", "regex": 'reliaquest.com:Admin'},
    {"name": "EP Deployed", "Location": "/store/configservices/deployed/deployment.xml", "regex": '1699'},
    {"name": "AH Deployed", "Location": "/store/configservices/deployed/deployment.xml", "regex": '4000'},
    {"name": "Migrated Apps to AH", "Location": "/var/log/qradar.log", "regex": '/console/restapi/api/gui_app_framework/migration/apphost/start'}
    # Add more tasks here
]
#----------------------------------------------------------------------------------------------------------------------------

# Validate Key Input
def keyValidation():
    ip_address = socket.gethostbyname(socket.gethostname())
    
    # b653e7c6-434c-4829-9b0c-518c45e876dd
    key_regex = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"

    print("\nIn order for the script to work, an Authorized Service Token must be made.\nPlease see the following link for more information: https://www.ibm.com/docs/en/qradar-common?topic=forwarding-creating-authentication-token\n")
    user_input = input("Please input authorization token: ")

    # Validate Key Format is correct
    while not re.match(key_regex, user_input):
        print("Incorrect Input Format...")
        sleep(0.5)
        user_input = input("Please input authorization token: ")

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

    # check if /home/ec2-user/.ariel_query/tokens/localhost.token exists if not:
    if os.path.isfile("/home/ec2-user/.ariel_query/tokens/localhost.token") == False:
        # Receive SEC_KEY and Validate the SEC_KEY works
        SEC_KEY = keyValidation()
        print("Saving token to /home/ec2-user/.ariel_query/tokens/localhost.token ...")


        # NOTE: THIS IS BREAKING, NEED TO FIGURE OUT HOW TO SEND TOKEN AFTER QUESTION
        child = pexpect.spawn('/opt/qradar/bin/ariel_query --query="SELECT payload, * FROM events WHERE qid=28250072 LAST 300 HOURS" --output JSON --save_token')
        sleep(0.1)
        child.sendline(SEC_KEY)
        
        
        
        print("Saved...")
        child.close()

    print("\nStarting validation check...\n")

    #----------------------------------------------------------------------------------------------------------------------------
    # Loop through internal dictionary lab steps and print results
    for task in INTERNAL:
        location = task['Location']
        name = task['name']
        regex_exp = task['regex']

        try:
            command = f'sudo grep "{regex_exp}" {location}'
            out = subprocess.check_output(command, shell=True)
            out = out.decode("ascii")

            if re.search(regex_exp, out):
                print(f"{name}: Pass")
            else:
                print(f"{name}: Failed")
        except:
            print(f"{name}: Failed")
    #----------------------------------------------------------------------------------------------------------------------------

    # NOTE: !!!!!!!!When running the script as sudo, it errors because the auth token was made in the user account and not root!!!!!!!!
    for task in EVENTS:
        qid = task["qid"]

        command = f'/opt/qradar/bin/ariel_query --query="SELECT payload, * FROM events WHERE qid={qid} LAST 200 HOURS" --output JSON'
        out = subprocess.check_output(command, shell=True)
        decoded = out.decode('ascii')

        # Parse out base64 payload
        regex_exp = r'payload":"(.*)"'

        # Use the regex expression to extract the matching string
        match = re.findall(regex_exp, decoded)

        # Extract the desired substring from the match object
        if match:
            found = 0
            # Decode the matched string from Base64 to UTF-8
            for b64_str in match:
                utf8_str = base64.b64decode(b64_str).decode('utf-8')
                match = re.search(task['regex'], utf8_str)
                if match:
                    print(f"{task['name']}: Pass")
                    found = 1
                    break
                else:
                    continue
            if found == 0:
                print(f"{task['name']}: Failed")
        else:
            print("Ariel Query failed: ", task["name"])

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
