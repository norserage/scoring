from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ScoringEngine.conf import conf

#engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')
engine = create_engine(conf['database'])
Session = sessionmaker(bind=engine)
