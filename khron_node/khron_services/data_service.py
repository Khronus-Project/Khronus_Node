from khron_node.data.models import Alert

def create_alert(request_ID: str, body:str) -> Alert:
    alert = Alert()
    alert.request_ID = request_ID
    alert.body = body
    alert.save()
    return alert

def find_alert_by_ID(request_ID: str) -> Alert:
    alert = Alert.objects(request_ID=request_ID).first()
    return alert