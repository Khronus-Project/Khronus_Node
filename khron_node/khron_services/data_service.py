from data.models import Base, Event, Event_Type, Task_Type, Khron_Request, Alert, Status
from data.database import engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import environ
import json

load_dotenv()
Session = sessionmaker(bind=engine)
session = Session()

def initialize_db():
    with open(environ["INITIAL_DATA"]) as f:
        initial_data = json.load(f)
    Base.metadata.create_all(engine)
    print('created_db')
    for _event_type in initial_data["Event_Types"]:
        curr_event_type = Event_Type(id=_event_type[0],event_type=_event_type[1])
        session.add(curr_event_type)
    print("loaded event types")
    for _task_type in initial_data["Task_Types"]:
        curr_task_type = Task_Type(id=_task_type[0],task_type=_task_type[1])
        session.add(curr_task_type)
    print("loaded task types")
    for _status in initial_data["Status"]:
        curr_status = Status(id=_status[0],status=_status[1])
        session.add(curr_status)
    print("loaded status")
    session.commit()
    print("DB Saved")
    return "Initial Tables Created"

def add_alert(_alert):
    try:
        added_alert = Alert(id=_alert['id'],parent=_alert['parent'],correlative=_alert['correlative'],timestamp=_alert['timestamp'],status_id=_alert['status_id'])
        session.add(added_alert)
        session.commit()
        print(f"added alert with {_alert}")
    except Exception as e:
        print(f"Alert {_alert} already processed just checking here")
        session.rollback()
    return True


def add_event(_event):
    added_event = Event(type_id=_event["type_id"],time=_event["time"],task_type_id=_event["task_type_id"], khron_request_id=_event["khron_request_id"], alert_id=_event["alert_id"])
    session.add(added_event)
    session.commit()
    print(f"event added with {_event}")
    return True

def query_alert(_timestamp):
    return session.query(Alert).filter_by(timestamp=_timestamp)

def modify_alert_status(_alert, status):
    _alert.status_id = status
    session.commit()