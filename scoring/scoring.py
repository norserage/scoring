import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')