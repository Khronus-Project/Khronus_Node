from posixpath import dirname
from sqlalchemy import create_engine
from os import mkdir, path, environ
from dotenv import load_dotenv

load_dotenv()
if not path.exists(environ['DATABASE_PATH']):
    mkdir(environ['DATABASE_PATH'])
    print(f"directory {environ['DATABASE_PATH']} created")

db_path = f"sqlite:///{environ['DATABASE_PATH']}/database.db"

engine = create_engine(db_path, echo=False)
