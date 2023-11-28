import socket
import os
import datetime
import signal
import sys
import json

# Read IP and port from config file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

SERVER_PORT = config_data['Server']['port']
SERVER_IP = config_data['Server']['ip']
LOG_FILE = config_data['Server']['log']

# Dictionary to store lists
lists = {}

# Function to close socket on Ctrl + C
def signal_handler(sig, frame):
    print("Sever is shutting down")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Function to log requests and responses
def log(entry, level='INFO'):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp} {entry} {level}\n"
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)
print(f"Server started on port {SERVER_PORT}")
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

while True:
    request = client_socket.recv(1024).decode('utf-8')
    log(f"REQUEST {request}", 'INFO')

    shutDown = False
    response = "NO-RESPONSE"

    # catalog command 
    if request == "catalog":
        if lists:
            response = "List of defined lists:\n"
            for i, list_title in enumerate(lists, start=1):
                response += f"{i}. {list_title}\n"

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')
        else:
            response = "No lists defined."

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')

    # create command 
    elif request.startswith("create "):
        list_title = request.split("create ")[1].strip()
        if list_title not in lists:
            lists[list_title] = []
            response = f"List '{list_title}' created successfully."

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')
        else:
            response = f"List '{list_title}' already exists."

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')


    # edit command
    elif request.startswith("edit "):
        list_title = request.split("edit ")[1].strip()
        if list_title in lists:
            response = f"Editing list '{list_title}'."
            edit_mode = True

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')


            # in edit mode
            while edit_mode:
                sub_command = client_socket.recv(1024).decode('utf-8')
                log(f"REQUEST {sub_command}", 'INFO')
                
                # show command
                if sub_command == "show":
                    response = f"List items for '{list_title}':\n"
                    for i, item in enumerate(lists[list_title], start=1):
                        response += f"{i}. {item}\n"


                    client_socket.send(response.encode('utf-8'))
                    log(f"RESPONSE {response}", 'INFO')
                
                # add command
                elif sub_command.startswith("add "):
                    item_text = sub_command.split("add ")[1].strip()
                    lists[list_title].append(item_text)
                    response = f"Added item '{item_text}' to list '{list_title}'."

                    client_socket.send(response.encode('utf-8'))
                    log(f"RESPONSE {response}", 'INFO')
                
                # remove command
                elif sub_command.startswith("remove "):
                    item_number = sub_command.split("remove ")[1].strip()
                    try:
                        item_number = int(item_number)
                        if 1 <= item_number <= len(lists[list_title]):
                            removed_item = lists[list_title].pop(item_number - 1)
                            response = f"Removed item '{removed_item}' from list '{list_title}'."
                            client_socket.send(response.encode('utf-8'))
                            log(f"RESPONSE {response}", 'INFO')
                        else:
                            response = "ERROR: Invalid item number."
                            client_socket.send(response.encode('utf-8'))
                            log(f"RESPONSE {response}", 'ERROR')
                    except ValueError:
                        response = f"ERROR: '{item_number}' is not a number.\nThe command should be of the format 'remove <item-number>'"
                        client_socket.send(response.encode('utf-8'))
                        log(f"RESPONSE {response}", 'ERROR')
                
                # quit edit mode
                elif sub_command == "quit":
                    response = "Exiting edit mode."
                    edit_mode = False

                    client_socket.send(response.encode('utf-8'))
                    log(f"RESPONSE {response}", 'INFO')
                else:
                    response = "ERROR: Invalid edit sub-command."

                    client_socket.send(response.encode('utf-8'))
                    log(f"RESPONSE {response}", 'ERROR')

                response = ""
        else:
            response = f"ERROR: a list does not exist by the name of '{list_title}'"
            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'ERROR')
    # display command
    elif request.startswith("display "):
        list_title = request.split("display ")[1].strip()
        if list_title in lists:
            response = f"Displaying items for list '{list_title}':\n"
            for i, item in enumerate(lists[list_title], start=1):
                response += f"{i}. {item}\n"
            
            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')
        else:
            response = f"List '{list_title}' does not exist"
            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'ERROR')

    # delete command 
    elif request.startswith("delete "):
        list_title = request.split("delete ")[1].strip()
        if list_title in lists:
            del lists[list_title]
            response = f"{list_title} has been deleted.\n"

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'INFO')
        else:
            response = "ERROR: List by that name does not exist."

            client_socket.send(response.encode('utf-8'))
            log(f"RESPONSE {response}", 'ERROR')

    # exit command 
    elif request == "exit":
        shutDown = True
        response = "Shutting down server..."

        client_socket.send(response.encode('utf-8'))
        log(f"RESPONSE {response}", 'INFO')
    else:
        response = "ERROR: Invalid command.\n\nValid commands are:\ncatalog\ncreate <list title>\nedit <list title>\ndisplay <list title>\ndelete <list title>\nedit\n"
        client_socket.send(response.encode('utf-8'))
        log(f"RESPONSE {response}", 'ERROR')
        

    
    # Send the response back to the client
    #client_socket.send(response.encode('utf-8'))
    #log(f"RESPONSE {response}", 'INFO')
    
    if shutDown:
        server_socket.close()
        sys.exit(0)
        break
    



# Clean up and close the server socket
server_socket.close()

