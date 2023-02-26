import socket
import pickle

# Set up client socket
host = 'localhost'
port = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Load local inventory from disk
try:
    with open('local_inventory.pickle', 'rb') as f:
        local_inventory = pickle.load(f)
except:
    local_inventory = {}

# Helper function to send requests to the server and receive responses


def send_request(request):
    data = pickle.dumps(request)
    client_socket.send(data)
    response_data = client_socket.recv(1024)
    response = pickle.loads(response_data)
    return response


# Main client loop
while True:
    # Display menu
    print("Please select an option:")
    print("1. Login")
    print("2. View current server inventory")
    print("3. View local inventory")
    print("4. Purchase items")
    print("5. Logout")
    choice = input("Enter your choice: ")

    # Process user choice
    if choice == '1':
        # Get login credentials from user
        username = input("Enter username: ")
        password = input("Enter password: ")
        request = {'type': 'login', 'username': username, 'password': password}
        response = send_request(request)
        print(response['message'])

    elif choice == '2':
        # Get current server inventory
        request = {'type': 'inventory'}
        response = send_request(request)
        if response['status'] == 'success':
            print("Current server inventory:")
            for upc, qty in response['inventory'].items():
                print(f"UPC: {upc}, Quantity: {qty}")
        else:
            print("Error getting server inventory.")

    elif choice == '3':
        # Show local inventory
        if len(local_inventory) == 0:
            print("Local inventory is empty.")
        else:
            print("Current local inventory:")
            for upc, qty in local_inventory.items():
                print(f"UPC: {upc}, Quantity: {qty}")

    elif choice == '4':
        # Purchase items
        if 'username' not in locals():
            print("You must log in first.")
        else:
            # Get item and quantity from user
            upc = int(input("Enter UPC of item to purchase: "))
            qty = int(input("Enter quantity to purchase: "))
            request = {'type': 'purchase', 'upc': upc, 'qty': qty}
            response = send_request(request)
            if response['status'] == 'success':
                print(response['message'])
                # Update local inventory
                if upc in local_inventory:
                    local_inventory[upc] += qty
                else:
                    local_inventory[upc] = qty
            else:
                print(response['message'])

    elif choice == '5':
        # Logout
        if 'username' not in locals():
            print("You are not currently logged in.")
        else:
            request = {'type': 'logout', 'username': username}
            response = send_request(request)
            print(response['message'])
            del username

    else:
        print("Invalid choice.")

    # Save local inventory to disk
    with open('local_inventory.pickle', 'wb') as f:
        pickle.dump(local_inventory, f)
