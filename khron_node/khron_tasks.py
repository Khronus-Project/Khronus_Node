from .celery import app
import os
from dotenv import load_dotenv
from web3 import Web3
import json
import time

with open ('./logfiles/results.json','w') as f:
    json.dump([], f)

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
    log_topic({'function':'handle event'})
    receipt = web3_connection.eth.waitForTransactionReceipt(event['transactionHash'])
    for log in receipt['logs']:
        log_topic({'function':'Enter loop in handle event'})
        if log['topics'][0].hex() == '0x68673052f6fb5d6e65ffb26edcd2394ed5509acfeaf07fe99909055f10767dfc':
            log_topic({'function':'Found right log'})
            log_of_interest = log
    result = event_of_interest.processLog(log_of_interest)
    log_topic(dict(result.args))

@app.task
def monitor_request(contract_address, abi_path):
    block_filter = web3_connection.eth.filter({'fromBlock':'latest','address':contract_address})
    block_filter_len = len(block_filter.get_new_entries())
    abi_path_flag = os.path.isfile(abi_path)
    log_topic({'function':'Monitor Request', 'New Entries':block_filter_len, 'contract':contract_address, 'ABI_File':abi_path_flag})
    for event in block_filter.get_new_entries():
        log_topic({'function':'Enter loop on monitor request'})
        handle_event(event, set_event(contract_address, abi_path))

@app.task
def my_background_task():
    entries = []
    entry = {'Time':time.time(), 'Topics':'No topic'}
    if not os.path.isfile('./logfiles/results.json'):
        entries.append(entry)
        with open('./logfiles/results.json', mode='w') as f:
            f.write(json.dumps(entries, indent=2))
    else:
        with open('./logfiles/results.json') as feedsjson:
            feeds = json.load(feedsjson)
            feeds.append(entry)
        with open('./logfiles/results.json', mode='w') as f:
            f.write(json.dumps(feeds, indent=2))
    return 'Done'

def log_topic(topics):
    entries = []
    entry = {'Time':time.time(), 'Topics':topics}
    if not os.path.isfile('./logfiles/results.json'):
        entries.append(entry)
        with open('./logfiles/results.json', mode='w') as f:
            f.write(json.dumps(entries, indent=2))
    else:
        with open('./logfiles/results.json') as feedsjson:
            feeds = json.load(feedsjson)
            feeds.append(entry)
        with open('./logfiles/results.json', mode='w') as f:
            f.write(json.dumps(feeds, indent=2))