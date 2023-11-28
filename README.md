# List Manager Project
## Introduction
The List Manager Project is a Python-based client-server application designed to manage multiple lists such as shopping or to-do lists. This project provides a hands-on exploration of internet network communication using socket programming in Python. The client and server applications interact using the TCP/IP communication stack.

## Project Structure
The project is divided into two main components:

### Server Application:

Implements a request/response type list server using Python through the command line.
Accepts and responds to commands for managing lists.
Maintains lists on the server.
### Client Application:

Custom client application to interact with the list manager server.
Accepts user commands, formats them into server requests, and displays server responses.
Supports commands for cataloging, creating, editing, displaying, deleting lists, and more.
## How to Run
## Server Application
1. Install Python:
Ensure you have Python installed on your system.

2. Run the Server:
python server.py

## Client Application
1. Install Python:
Ensure you have Python installed on your system.

2. Run the Client:
python client.py


## Configuration
The server's IP address and port are set in the config.json file.
{
  "Server": {
    "port": 12000
  }
}


## Contributors

Charlie Vukovic

Nick Boenau
