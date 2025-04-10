from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_CONNECTION = "mysql+pymysql://root:1234@localhost/test"

engine = create_engine(URL_CONNECTION)

localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()