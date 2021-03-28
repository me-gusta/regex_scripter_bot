from regex_scripter.database.db import Base, engine

Base.metadata.create_all(engine)
