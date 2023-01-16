# Khronus Protocol Node Application

## Running Local Validator

This is the validator necessary to run the validator test in the local network. 
- Clone the repository
- Make sure that the contracts are deployed in the local network. 
- Create a .env file with the data required in the .env-template file. (Deployed contracts, private key and rpc nodes are needed).
    - Deployed address of your locally deployed Khronus Node contract
    - Private to be used by the node
    - local rpc network link
- From the main directory where the project was cloned:
    - Create a virtual environment with python 3
    - switch to the virtual environment 
    - Pip install -r requirements.txt
    - python khron_node/initialize_node.py
    - python khron_node/node_operator.py <network that you want to connect>

## Containerized Validator
### Dependencies
    - Docker is needed to built a containerized validator
### Process
    - Create a .env file with the data required in the .env-template file. (Deployed contracts and rpc nodes are needed).
    - from the folder where the project was cloned:
        - run: docker build -f ./build/Dockerfile-mumbai -t khronus-node-mumbai .
            - Where -f points to the docker file that will serve as a base for the image. 
            - The name of the docker file points to the network the image will connect when deployed.
            - Image to local will fail since there is no ganache network rpc active in the image.
    - A container based on the image can be built from the docker application 

## Alpha Validitor
    - The protocol is only running on Mumbai Testnet of Polygon
    - To run an alpha validator you will need the following
        - Deploy your own node contract. The contract should inherit from the Khronus Utils https://github.com/Khronus-Project/Khronus_utils/blob/master/contracts/KhronusNodeBase.sol
            - For deploying you need the coordinator contract address, the current Alpha coordinator is at: 0xdf75F4D728812d76113a48E0da18F3AfA96E5179
    - Deploy a virtual machine with an infrastructure provider.
        - SSH on your virtual machine 
        - Clone this repository in a directory in your VM
        - Install python 3.9 in the VM, currently the dependencies don't work well with Python 3.10
        - Prepare your enviroment variables file according to the template at .example_env
            - You will need a node provider that allows to create filters.
            - For mumbai Alchemy has a free node that works for this. 
        - Create a virtual environment
        - Switch to the virtual environment 
        - Pip install the dependencies in the requirements.txt file.
            If there are errors it might have to do with the version of python not being 3.9 but 3.10. If you see errors contact us at: khronus-project@outlook.com
        - Once all of the dependencies are installed:
            - Launch the console
                - run python khron_node/initialize_node.py
                - Start tmux by typing tmux into the shell
                - In tmux run python khron_node/node_operator.py mumbai
                - leave/detach the tmux session by typing Ctrl+b and then d
            - You can safely close your console.



