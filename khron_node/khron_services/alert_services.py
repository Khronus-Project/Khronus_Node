from queue import Empty
from khron_services.byte_services import decode, get_action_type
from khron_services.data_services import add_alert, add_event, query_alerts, modify_alert_status
from khron_services.web3_services import get_node_contract, fulfill_alert, get_blockchain_timestamp
from datetime import datetime, timezone

# Request processor functions

# Entry point interface
def handle_request_event(event):
    request = dict(event.args)
    processed_request = process_request(request["data"])

def process_request(_request):
    action_type = get_action_type(_request)
    request_content = decode(_request,action_type)
    dispatcher(action_type)(request_content)

def dispatcher(_action_type):
    processing_routines = {
        "102":create_alert
    }
    return processing_routines[_action_type]

def create_alert(_request_content):
    crud_event_type = "1" #see data configurations initial tables json
    task_type = "02" #see data configuration initial tables json
    khron_request_id = "" # not applicable to alerts
    alert = {"id":_request_content["alertID"],'parent':_request_content['requestID'],'correlative':_request_content['alert_correlative'],'timestamp':_request_content["timestamp"], "status_id":"01"}
    event = {"type_id":crud_event_type,"time":datetime.now(timezone.utc),"task_type_id":task_type, "khron_request_id":khron_request_id, "alert_id":_request_content["alertID"]}
    add_alert(alert)
    add_event(event)
    return True

# Alert servicing processor functions

def get_current_alerts(_timestamp):
    alerts = query_alerts(_timestamp)
    print(f"current timestamp is {_timestamp}, upperlimit exclusive is {_timestamp+60}")
    return alerts

def trigger_alert(alert):
    contract = get_node_contract()
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