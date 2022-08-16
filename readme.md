# Khronus Protocol Node Application

## Running Local Validator

This is the validator necessary to run the validator test in the local network. 
- Clone the repository
- Make sure that the contracts are deployed in the local network. 
- Create a .env file with the data required in the .env-template file. (Deployed contracts and rpc nodes are needed).
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

## Development Environment (To be reviewed)
    - Push the desired image to a container registry
    - Build container in the cloud based in the image



