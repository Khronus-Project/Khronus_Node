from khron_node.khron_services.data_service import query_alert

def trigger_alert(_timestamp):
    alerts = query_alert(_timestamp)
    for alert in alerts:
        print(alert.id)