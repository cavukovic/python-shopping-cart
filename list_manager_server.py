import socket
import os
import datetime
import signal
import sys

SERVER_IP = '127.0.0.1'  # server's IP address
SERVER_PORT = 12000  # server port
LOG_FILE = 'server.log'

# Dictionary to store lists
lists = {}

# Function to close socket on Ctrl + C
def signal_handler(sig, frame):
    print("Shutting down server...")
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

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    
    request = client_socket.recv(1024).decode('utf-8')
    log(f"REQUEST {request}", 'INFO')

    # need to process the request and generate a response
    response = "this is a test"
    
    # Send the response back to the client
    client_socket.send(response.encode('utf-8'))
    
    log(f"RESPONSE {response}", 'INFO')
    
    client_socket.close()

# Clean up and close the server socket
server_socket.close()

