import socket
import sys
import json

# Read IP and port from config file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

SERVER_PORT = config_data['Server']['port']
SERVER_IP = config_data['Server']['ip']

# create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Function to send a request to the server
def send_request(request):
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    return response

while True:
    command = input("Enter a command: ")
    sys.stdout.flush()
    
    # Send the command to the server
    response = send_request(command)

    # Process the response and display it
    print(response)

    if command == 'exit':
        client_socket.close()
        break

# Close the client socket
client_socket.close()
