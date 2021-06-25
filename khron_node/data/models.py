import mongoengine
import datetime

class Alert(mongoengine.Document):
    registered_date=mongoengine.DateField(default=datetime.datetime.now(datetime.timezone.utc))
    request_ID = mongoengine.StringField()
    body = mongoengine.StringField()

    meta = {
        'db_alias':'core',
        'collection':'alerts'
    }


