import asyncio
from khron_services.request_processor import process_request
from khron_services.alert_processor import trigger_alert
from khron_services.web3_service import get_node_contract, get_event_filter, initialize_configs
from datetime import datetime
import sys

network = sys.argv

def main(options):
    initialize_configs(options[1])
    listen()

def handle_event(event):
    request = dict(event.args)
    processed_request = process_request(request["data"])

async def log_loop(event_filter):
    while True:
        try:
            events = event_filter.get_new_entries()
            for event in events:
                handle_event(event)
        except Exception as e:
            print("network is a bit slow")
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

def listen():
    contract = get_node_contract()
    event_filter = get_event_filter(contract)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(event_filter),check_time()))
    finally:
        loop.close()

main(network)