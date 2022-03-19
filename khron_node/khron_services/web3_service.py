from os import environ
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import json

load_dotenv()

def initialize_configs(network):
    global config_node_provider 
    global config_abiPath 
    global config_nodeContractAddress 
    global config_nodePrivateKey 
    global web3_connection
    if network == "local":
        config_node_provider = environ['NODE_PROVIDER_LOCAL']
        config_abiPath = environ["ABI_PATH_LOCAL"]
        config_nodeContractAddress = environ["ADDRESS_LOCAL"]
        config_nodePrivateKey = environ["PRIVATE_KEY_LOCAL"]
        web3_connection = Web3(Web3.HTTPProvider(config_node_provider))
        set_POA_middleware()
        print(f'connected {network}')
    elif network == "rinkeby":
        config_node_provider = environ['NODE_PROVIDER_RINKY']
        config_abiPath = environ["ABI_PATH_DEPLOYED"]
        config_nodeContractAddress = environ["ADDRESS_RINKY"]
        config_nodePrivateKey = environ["PRIVATE_KEY_DEPLOYED"]
        web3_connection = Web3(Web3.HTTPProvider(config_node_provider))
        set_POA_middleware()
        print(f'connected {network}')
    elif network == "bsc_test":
        config_node_provider = environ['NODE_PROVIDER_BSC_OFFICIAL']
        config_abiPath = environ["ABI_PATH_DEPLOYED"]
        config_nodeContractAddress = environ["ADDRESS_BSC"]
        config_nodePrivateKey = environ["PRIVATE_KEY_DEPLOYED"]
        web3_connection = Web3(Web3.HTTPProvider(config_node_provider))
        set_POA_middleware()
        print(f'connected {network}')
    elif network == "ropsten":
        config_node_provider = environ['NODE_PROVIDER_ROPSTEN']
        config_abiPath = environ["ABI_PATH_DEPLOYED"]
        config_nodeContractAddress = environ["ADDRESS_ROPTSTEN"]
        config_nodePrivateKey = environ["PRIVATE_KEY_DEPLOYED"]
        web3_connection = Web3(Web3.HTTPProvider(config_node_provider))
        set_POA_middleware()
        print(f'connected {network}')
    else:
        print("Unsoported Network")

def are_we_connected():
    return web3_connection.isConnected()

def get_node_contract():
    try:
        with open(config_abiPath) as f:
            abiJson = json.load(f)
        contract = web3_connection.eth.contract(address=config_nodeContractAddress, abi=abiJson['abi'])
        return contract
    except Exception as e:
        print (e, config_abiPath)

def get_event_filter(contract):
    are_we_connected()
    return contract.events.RequestReceived.createFilter(fromBlock='latest')

def fulfill_alert(contract, alertID):
    estimated_gas = contract.functions.fulfillAlert(alertID).estimateGas()
    if estimated_gas <= 450000:
        transaction_body = {
            "nonce":web3_connection.eth.get_transaction_count(get_public_key()),
            "gas":150000
        }
        function_call = contract.functions.fulfillAlert(alertID).buildTransaction(transaction_body)
        print(f'Estimated gas to fulfill alert {contract.functions.fulfillAlert(alertID).estimateGas()}')
        signed_transaction = web3_connection.eth.account.sign_transaction(function_call, config_nodePrivateKey)
        fulfill_tx = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
        result = fulfill_tx
    else:
        result = {"Exception":"0001", "Description":"f'alertID {alertID} exceeds the allowed gas limit of 450000 units"}
    return result

def get_public_key():
    account = web3_connection.eth.account.from_key(config_nodePrivateKey)
    return account.address


def get_node_provider():
    return (config_node_provider)

def get_blockchain_timestamp():
    return web3_connection.eth.get_block("latest").timestamp

def set_POA_middleware():
    web3_connection.middleware_onion.inject(geth_poa_middleware, layer=0)