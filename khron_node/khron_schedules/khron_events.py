import os
from dotenv import load_dotenv
from web3 import Web3
import json

load_dotenv()
node_provider = os.environ['NODE_PROVIDER']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

def set_event(contract_address, abi_path):
    with open(abi_path) as f:
        abiJson = json.load(f)
    contract = web3_connection.eth.contract(address=contract_address, abi=abiJson['abi'])
    event_of_interest = contract.events.RequestReceived()
    return event_of_interest

def handle_event(event, event_of_interest):
    receipt = web3_connection.eth.waitForTransactionReceipt(event['transactionHash'])
    for log in receipt['logs']:
        if log['topics'][0].hex() == '0x68673052f6fb5d6e65ffb26edcd2394ed5509acfeaf07fe99909055f10767dfc':
            log_of_interest = log
    result = event_of_interest.processLog(log_of_interest)
    print(result)

@khron_tasks.task
def monitor_request(event_filter, event_of_interest):
    for event in event_filter.get_new_entries():
        handle_event(event, event_of_interest)

@khron_tasks.task
def my_background_task(arg1, arg2):
    result = arg1+arg2
    return result

def listen(contract_address, abi_path):
    block_filter = web3_connection.eth.filter({'fromBlock':'latest','address':contract_address})
    for event in block_filter.get_new_entries():
        handle_event(event, set_event(contract_address, abi_path))
    
    khron_tasks.conf.beat_schedule = {
    #Executes every 2 minutes
    'Monitor_request': {
            'task': 'khron_task.monitor_request',
            'schedule': crontab(minute='*/2'),
            'args': (block_filter, set_event(contract_address, abi_path)),
        },
    }
