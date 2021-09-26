from os import environ
from web3 import Web3
from dotenv import load_dotenv
import json

from web3.types import SignedTx

load_dotenv()
node_provider = environ['NODE_PROVIDER']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

def are_we_connected():
    return web3_connection.isConnected()

def get_node_contract():
    with open(environ["ABI_PATH"]) as f:
        abiJson = json.load(f)
    contract = web3_connection.eth.contract(address=environ["ADDRESS"], abi=abiJson['abi'])
    return contract

def get_event_filter(contract):
    return contract.events.RequestReceived.createFilter(fromBlock='latest')

def fulfill_alert(contract, alertID):
    estimated_gas = estimateAlertGas(contract, alertID)
    if estimated_gas <= 450000:
        transaction_body = {
            "nonce":web3_connection.eth.get_transaction_count(getPublicKey()),
            'gas': estimated_gas,
            'gasPrice': web3_connection.toWei('1', 'gwei')
        }
        function_call = contract.functions.fulfillAlert(alertID).buildTransaction(transaction_body)
        signed_transaction = web3_connection.eth.account.sign_transaction(function_call, environ['PRIVATE_KEY'])
        fulfill_tx = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
        txt_receipt = web3_connection.eth.get_transaction_receipt(fulfill_tx)
        result = txt_receipt.logs
    else:
        result = {"Exception":"0001", "Description":"f'alertID {alertID} exceeds the allowed gas limit of 450000 units"}
    return result

def estimateAlertGas(contract, alertID):
    transaction_body = {
        "nonce":web3_connection.eth.get_transaction_count(getPublicKey()),
        "to":contract.address,
        "from":getPublicKey(),
        "data":contract.encodeABI(fn_name="fulfillAlert", args=[alertID])
    }
    return web3_connection.eth.estimate_gas(transaction_body) + 10000

def getPublicKey():
    #test = web3_connection.eth.account.privateKeyToAccount(environ['PRIVATE_KEY'])
    test = web3_connection.eth.account.from_key(environ['PRIVATE_KEY'])
    return test.address