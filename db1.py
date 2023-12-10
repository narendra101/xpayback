# postgress database configuration, default=uuid.uuid4, primary_key=True
from sqlalchemy import create_engine, Column, String, LargeBinary, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()
DB_URL = "postgresql://<username>:<password>@<host>:<port>/<database_name>"
# test url = "postgresql://postgres:postgres@localhost:5432/test"

class User(Base):
    __tablename__ = 'User'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(String(80))
    email = Column(String(80))
    password = Column(String(255))
    phone = Column(String(20))

class UserDB:
    def __init__(self, database_url: str = DB_URL):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def add_user(self, full_name: str, email: str, password: str, phone: str, user_id: str) -> dict:
        session = self.SessionLocal()
        
        if session.query(User).filter_by(email=email).first():
            session.close()
            return {'status': 'error', 'message': "Email already exists"}
        
        new_user = User(
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            user_id=user_id
        )
        session.add(new_user)
        session.commit()
        session.close()

        return {'status': 'success', 'message': 'User added successfully'}
    
    def get_user(self, email: str, password: str):
        session = self.SessionLocal()
        user = session.query(User).filter(and_(User.email == email, User.password == password)).first()
        session.close()

        if user:
            return {'status': 'success', 'user_details': {
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'user_id': str(user.user_id),
                'password': user.password
            }}
        else:
            return {'status': 'error', 'message': 'User not found'}


# mongodb configuration

import pymongo
IMAGE_DATABASE = 'image_db'
IMAGE_COLLECTION = 'image_collection'
client = pymongo.MongoClient('localhost', 27017)
image_db = client[IMAGE_DATABASE][IMAGE_COLLECTION]

