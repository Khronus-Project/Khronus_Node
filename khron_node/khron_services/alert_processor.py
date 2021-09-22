from khron_node.khron_services.data_service import query_alert, modify_alert_status

def trigger_alert(_timestamp):
    alerts = query_alert(_timestamp)
    for alert in alerts:
        modify_alert_status(alert,"02")
        print(alert.id)