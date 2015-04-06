from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')
engine = create_engine('postgresql://scoring:scoring@10.151.9.11/scoring')
Session = sessionmaker(bind=engine)
