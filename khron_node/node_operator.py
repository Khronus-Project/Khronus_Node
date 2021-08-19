from os import environ
from web3 import Web3
from dotenv import load_dotenv
import json
import asyncio
from khron_node.khron_services.request_processor import process_request
from khron_node.khron_services.alert_processor import trigger_alert
from datetime import datetime

load_dotenv()
node_provider = environ['NODE_PROVIDER']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

def are_we_connected():
    return web3_connection.isConnected()

def handle_event(event):
    request = dict(event.args)
    processed_request = process_request(request["data"])

async def log_loop(event_filter):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(5)

async def check_time():
    while True:
        currtime = int(datetime.utcnow().timestamp())
        seconds_from_prev = currtime%60
        if seconds_from_prev == 0:
            trigger_alert(datetime.fromtimestamp(currtime))
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(60-seconds_from_prev)

def listen(contract_address, abi_path):
    with open(abi_path) as f:
        abiJson = json.load(f)
    contract = web3_connection.eth.contract(address=contract_address, abi=abiJson['abi'])
    event_filter = contract.events.RequestReceived.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(event_filter),check_time()))
    finally:
        loop.close()