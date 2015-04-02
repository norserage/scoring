from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
#engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')
engine = create_engine('postgresql://scoring:scoring@10.151.9.11/scoring')
=======
engine = create_engine('mysql://scoring:scoring@10.151.9.11/scoring')
>>>>>>> b362ea7536dc0f626bacde5432b7c89e894345ef
Session = sessionmaker(bind=engine)
session = Session()