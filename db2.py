from sqlalchemy import create_engine, Column, String, LargeBinary, and_, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()
DB_URL = "postgresql://<username>:<password>@<host>:<port>/<database_name>"
server_url = '***'
# Ex server_url = "http://127.0.0.1:7000"

class User(Base):
    __tablename__ = 'User2'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(String(80))
    email = Column(String(80))
    password = Column(String(255))
    phone = Column(String(20))
    # image = relationship('ProfilePicture', backref='img')

class ProfilePicture(Base):
    __tablename__ = 'profile_picture'

    user_id = Column(UUID(as_uuid=True), ForeignKey('User2.user_id'), primary_key=True)
    image = Column(LargeBinary)
    file_name = Column(String(255))    

    # img = relationship('User', backref='profile_picture')
    

class UserDB:
    def __init__(self, database_url: str = DB_URL):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def add_user(self, full_name: str, email: str, password: str, phone: str, user_id: str, image: bytes, file_name: str) -> dict:
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

        new_profile_picture = ProfilePicture(
            user_id=user_id,
            image=image,
            file_name=file_name
        )

        session.add(new_user)
        session.commit()
        session.add(new_profile_picture)
        session.commit()        
        session.close()

        return {'status': 'success', 'message': 'User added successfully'}
    
    def get_user(self, email: str, password: str):
        session = self.SessionLocal()
        user = session.query(User).filter(and_(User.email == email, User.password == password)).first()
        session.close()
        image_details = session.query(ProfilePicture).filter(ProfilePicture.user_id == str(user.user_id)).first()

        if image_details:
            with open(image_details.file_name, 'wb') as f:
                f.write(image_details.image)

        if user:
            return {'status': 'success', 'user_details': {
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'user_id': str(user.user_id),
                'password': user.password,
                'profile_source': f'{server_url}/get_image/{str(user.user_id)}/{image_details.file_name}'
            }}
        else:
            return {'status': 'error', 'message': 'User not found'}
