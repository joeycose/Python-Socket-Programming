import socket
import pickle

# Hardcoded user ids and passwords
users = {"user1": "password1", "user2": "password2", "user3": "password3"}

# Hardcoded initial inventory
inventory = {1: 10, 2: 5, 3: 8}

# Set up server socket
host = 'localhost'
port = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

# Helper function to handle purchase requests


def handle_purchase_request(upc, qty):
    if upc in inventory and inventory[upc] >= qty:
        inventory[upc] -= qty
        response = {'status': 'success',
                    'message': f'Purchase of {qty} units of item {upc} successful.'}
    else:
        response = {'status': 'failure',
                    'message': f'Purchase of {qty} units of item {upc} failed. Not enough units available.'}
    return response

# Helper function to handle inventory requests


def handle_inventory_request():
    response = {'status': 'success', 'inventory': inventory}
    return response

# Helper function to handle login requests


def handle_login_request(data):
    username = data['username']
    password = data['password']
    if username in users and users[username] == password:
        response = {'status': 'success', 'message': 'Login successful.'}
    else:
        response = {'status': 'failure',
                    'message': 'Login failed. Incorrect username or password.'}
    return response

# Helper function to handle logout requests


def handle_logout_request(data):
    username = data['username']
    del data['username']
    response = {'status': 'success', 'message': 'Logout successful.'}
    return response


# Main server loop
while True:
    # Wait for client to connect
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    # Receive data from client
    data = client_socket.recv(1024)
    request = pickle.loads(data)

    # Handle request
    if request['type'] == 'purchase':
        response = handle_purchase_request(request['upc'], request['qty'])
    elif request['type'] == 'inventory':
        response = handle_inventory_request()
    elif request['type'] == 'login':
        response = handle_login_request(request)
    elif request['type'] == 'logout':
        response = handle_logout_request(request)
    else:
        response = {'status': 'failure', 'message': 'Invalid request type.'}

    # Send response to client
    data = pickle.dumps(response)
    client_socket.send(data)

    # Close connection
    client_socket.close()
