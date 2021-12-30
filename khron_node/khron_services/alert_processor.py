from khron_services.data_service import query_alert, modify_alert_status
from khron_services.web3_service import get_node_contract, fulfill_alert, get_blockchain_timestamp
from datetime import datetime, timezone
from time import sleep

def trigger_alert(_timestamp):
    contract = get_node_contract()
    alerts = query_alert(_timestamp)
    for alert in alerts:
        modify_alert_status(alert,"02")
        print(alert.id)
        alertID = alert.id
        try:
            tx = fulfill_alert(contract,alertID)
            modify_alert_status(alert,"03")
            print(f'transaction hash is {tx.hex()}')
        except Exception as e:
            print(e)

def get_time_alignment():
    blockchain_timestamp = get_blockchain_timestamp()
    current_time = int(datetime.timestamp(datetime.now(timezone.utc)))
    if current_time > blockchain_timestamp:
        time_difference = current_time - blockchain_timestamp
        print(f'Current time is {current_time}, current block timestamp is {blockchain_timestamp}, waiting for a difference of {time_difference}')
    else:
        print('times are aligned')

    ## Need to build functionality to read the logs and if it is a failed transaction be able to compare the times in the logs