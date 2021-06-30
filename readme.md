# Khronus Protocol Node Application
## Description
The node application will be ran by all nodes in the Khronus protocol. The node application will be configured to listen to an specific node contract with which it will interact to resolve request.t
## The Application
- Currently the application works by listening to an specific node contract address. This address has to be referenced, and constantly updated, in the .env file, as ADDRESS. 
- When a request is received the node application will store the request in its database (mongo DB at the moment), if the request contains the data "this is real" it will print to the python console.
- All requests are designed to come from the send_events scripts in the contracts repository.
## The development environment
To run the current node application
1. Clone this repository.
2. The repository should be cloned under the same parent directory as the contracts repository.
3. Create and inititiate a virtual environment
4. Install the requirements.txt dependencies.
5. Install mongo Db in your system, and start the service.
6. Run the event_prep.py brownie script in the contracts repository and environment.
7. Copy the updated NodeContract address that appears in the contract_library folder contract_address.json document to the .env file of this repository.
8. Enter the python console
9. In the python console execute 'khron_node.listener import *'
10. In the python console execute 'listen(os.environ['ADDRESS'],os.environ['ABI_PATH'])'
11. The listener will start.
12. When you run the send_events.py brownie scripts in the contracts repository, the listener will react according to the request received.