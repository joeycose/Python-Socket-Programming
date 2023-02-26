# Python-Socket-Programming
client.py and server.py using python and pickle

Implement a client and web server which manages an inventory of products using Python's socket module.
server process
contains a data structure which stores client user ids and passwords. There is no need implement any security features. For simplicity, the user list can be hardcoded and does not need to be editable.

maintains an inventory of items. Each item is uniquely identified by a UPC code (you can simulate this with an integer value). You should track the current number of units available for each item. Like the user data structure, the product list should be hardcoded and not editable. When the system first starts, you can hardcode an initial number available for each item. Functionality to restock items is not required.
accepts the following request types from its clients via a socket connection.

accepts user login. The system should track when users are logged in. Login occurs when a client submits a user id password pair that is found in the user id data structure
accept purchase requests. Only logged in users can purchase items. Upon a purchase request, the server responds with a positive acknowldgement message along with the amount purchased and reduces the inventory for that item. Orders that can not be filled are refused and a negative message is included in response.

accepts request to view current inventory. Only logged in users can view inventory. This request should be fulfilled with a response which includes all the items maintained along with the current levels available.
accepts user logout. Any record maintaining the user login information should be deleted.
Inventory levels and login must be persisted to disk during shutdown so that they can be restored upon startup.

client process
provides a text based interface with the following options

user login
view current server inventory
view local inventory
purchase items, (if successful, items are stored in the local inventory)
logout
opens socket and sends requests to server (for options that require it). Responses should be displayed to the user.

Local inventory keeps track of what products have been obtained by the user. It must be persisted to a local disk during shutdown so that they can be restored upon startup.
