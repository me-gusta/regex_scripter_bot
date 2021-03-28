from database.db import Base, engine, session
Base.metadata.create_all(engine)
