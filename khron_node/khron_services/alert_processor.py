from khron_services.data_service import query_alert, modify_alert_status
from khron_services.web3_service import get_node_contract, fulfill_alert
from datetime import datetime, timezone

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
            print(int(datetime.timestamp(datetime.now(timezone.utc))))
            print(tx.hex())
        except Exception as e:
            print(e)
       

    ## Need to build functionality to read the logs and if it is a failed transaction be able to compare the times in the logs