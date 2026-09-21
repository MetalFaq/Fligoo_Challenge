from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# relative file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./fligoo_app.db" #define the file where SQLite will persist data. 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    #required for sqlite: Cause FastAPI can access the DB with multiple threads during a single request.
    connect_args={"check_same_thread": False}, 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Creation of DB Session. The session object is my main access point to the DB. 

Base = declarative_base() #Base class, from which all DB model classes will inherit. 


# Assign the session object to a variable.
def get_db():
    try:
        db = SessionLocal()
        yield db #create a single session for each request. 
    finally:
        db.close()
        