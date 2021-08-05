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
    #decode_hex = request['data'][2:].decode("ASCII")
    #request_JSON = json.loads(request['data'].decode("utf-8"))
    #print(request['_sender'],request_JSON)
    print(len(request['data']))
    print(request['data'][0:32].hex(), request['data'][32:64].hex(), request['data'][64:96].hex())
    print(int.from_bytes(request['data'][0:32],"little"), request['data'][32:64].hex(), int(request['data'][64:96].hex(),16))

async def log_loop(event_filter):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(5)

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