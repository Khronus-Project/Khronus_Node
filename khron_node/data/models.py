from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()

#-----------------------
class Event_Type(Base):
    __tablename__ = 'event_types'

    id = Column(String(1), primary_key=True)
    event_type = Column(String(10))

#-----------------------
class Task_Type(Base):
    __tablename__ = 'task_types'

    id = Column(String(2), primary_key=True)
    task_type = Column(String(10))

#-----------------------
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    time = Column(TIMESTAMP)
    type_id = Column(String(2), ForeignKey('event_types.id'))
    task_type_id = Column(String(2),ForeignKey('task_types.id'))
    khron_request_id = Column(String(64),ForeignKey('khron_requests.id'))
    alert_id = Column(String(64),ForeignKey('alerts.id'))
#-----------------------
class Khron_Request(Base):
    __tablename__ = 'khron_requests'
    
    id = Column(String(64), primary_key=True)
    iterations = Column(Integer)
    cron_tab = Column(String(10))
    status_id = Column(String(10),ForeignKey('status.id'))

#-----------------------
class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(String(64), primary_key=True)
    parent = Column(String(64))
    correlative = Column(Integer)
    timestamp = Column(TIMESTAMP, index=True)
    status_id = Column(String(2),ForeignKey('status.id'))

#-----------------------
class Status(Base):
    __tablename__ = 'status'

    id = Column(String(2), primary_key=True)
    status = Column(String(10))