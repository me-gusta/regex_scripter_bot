from sqlalchemy import create_engine

engine = create_engine('mysql+pymsql://regex:examplepassword@db:3306/regex_scripter')