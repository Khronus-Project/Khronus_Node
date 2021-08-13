from sqlalchemy import create_engine


engine = create_engine('sqlite:///khron_node/data/database.db', echo=True)

