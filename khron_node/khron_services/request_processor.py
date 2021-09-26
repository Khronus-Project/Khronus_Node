from khron_node.khron_services.byte_services import decode, get_action_type
from khron_node.khron_services.data_service import add_alert, add_event
from datetime import datetime, time, timezone

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
    alert = {"id":_request_content["alertID"],'parent':_request_content['requestID'],'correlative':_request_content['alert_correlative'],'timestamp':datetime.fromtimestamp(_request_content["timestamp"], timezone.utc), "status_id":"01"}
    event = {"type_id":crud_event_type,"time":datetime.now(timezone.utc),"task_type_id":task_type, "khron_request_id":khron_request_id, "alert_id":_request_content["alertID"]}
    add_alert(alert)
    add_event(event)
    return True

