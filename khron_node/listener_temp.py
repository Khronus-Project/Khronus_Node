import os
from web3 import Web3
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()
node_provider = os.environ['NODE_PROVIDER']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

def are_we_connected():
    return web3_connection.isConnected()

def handle_event(event):
    request = dict(event.args)
    request_JSON = json.loads(request['_data'].decode("utf-8"))
    print(request['_sender'],request_JSON)

async def log_loop(event_filter):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(20)

def listen(contract_address, abi_path):
    with open(abi_path) as f:
        abiJson = json.load(f)
    contract = web3_connection.eth.contract(address=contract_address, abi=abiJson['abi'])
    event_filter = contract.events.RequestReceived.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(event_filter)))
    finally:
        loop.close()