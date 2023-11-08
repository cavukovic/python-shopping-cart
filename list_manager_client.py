import socket
import sys

SERVER_IP = '127.0.0.1'  # Server's IP address
SERVER_PORT = 12000  # Server port

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
    
    # Send the command to the server
    response = send_request(command)

    # Process the response and display it
    print(response)

    if command == 'exit':
        break

# Close the client socket
client_socket.close()
