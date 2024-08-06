from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQL_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database>'
SQL_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQL_DATABASE_URL)

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()




# try:
#     conn = psycopg.connect(host="localhost",
#                            dbname="fastapi",
#                            user="postgres",
#                            password="admin",
#                            row_factory=dict_row
#                            )
#     cursor = conn.cursor()
#     print("database connected")
#     # break
# except Exception as error:
#     print("database connection failed")
#     print("Error", error)
#     time.sleep(2)


# while True: