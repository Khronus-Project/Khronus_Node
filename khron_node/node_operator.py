import asyncio
from khron_services.alert_services import handle_request_event, trigger_alert, get_current_alerts
from khron_services.web3_services import get_node_contract, get_event_filter, initialize_configs, get_blockchain_timestamp
from datetime import datetime, timezone
import sys

network = sys.argv

def main(options):
    initialize_configs(options[1])
    initialize_queue()
    listen()

async def log_loop():
    contract = get_node_contract()
    event_filter = get_event_filter(contract)
    while True:
        try:
            events = event_filter.get_new_entries()
            for event in events:
                handle_request_event(event)
        except Exception as e:
            print(f"exception is {e}")
        await asyncio.sleep(5)

async def khron_ticker():
    while True:
        currtime = int(datetime.timestamp(datetime.now(timezone.utc)))
        seconds_from_prev = currtime%60
        if seconds_from_prev == 0:
            alerts = get_current_alerts(currtime)
            if alerts == None:
                pass
            else:
                for alert in alerts:
                    await populate_alert_queue(alert)
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(60-seconds_from_prev)

async def populate_alert_queue(alert):
    await alerts_queue.put(alert)

async def serve_alert_queue():
    while True:
        alert = await alerts_queue.get()
        if alert is None:
            pass
        else:
            print(f"Currently serving alert ID {alert.id}")
            await get_time_alignment(alert)
            await async_trigger_alert(alert)

async def get_time_alignment(alert):
    blockchain_timestamp = get_blockchain_timestamp()
    if blockchain_timestamp < alert.timestamp:
        await alerts_queue.put(alert)

async def async_trigger_alert(alert):
    trigger_alert(alert)

def initialize_queue():
    global alerts_queue 
    alerts_queue = asyncio.Queue()

def listen():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(),khron_ticker(),serve_alert_queue()))
    finally:
        loop.close()

main(network)