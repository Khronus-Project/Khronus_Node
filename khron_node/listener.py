import os
from web3 import Web3
from dotenv import load_dotenv
import json
import asyncio
import khron_node.data.database as mongo_setup
import khron_node.khron_services.data_service as svc
mongo_setup.global_init()

load_dotenv()
node_provider = os.environ['NODE_PROVIDER']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

def are_we_connected():
    return web3_connection.isConnected()

def handle_event(event):
    request = dict(event.args)
    svc.create_alert(request['_data'].decode("utf-8"),request['_sender'])

async def log_loop(event_filter):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(20)

async def create_entry():
    while True:
        is_request = svc.find_alert_by_ID("this is real")
        if is_request != None:
            print("Triggering alarm")
        await asyncio.sleep(30)

def listen(contract_address, abi_path):
    with open(abi_path) as f:
        abiJson = json.load(f)
    contract = web3_connection.eth.contract(address=contract_address, abi=abiJson['abi'])
    event_filter = contract.events.RequestReceived.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(event_filter),create_entry()))
    finally:
        loop.close()




#svc.create_alert("DanielTest01","This is an alert")

#testing = svc.find_alert_by_ID("DanielTest01")

#print(testing)