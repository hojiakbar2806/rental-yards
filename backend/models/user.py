from database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)  # `bytes` o'rniga `String` ishlatilgan
    property_id = Column(Integer, ForeignKey('properties.id'))  # Property uchun tashqi kalit

    property = relationship("Property", back_populates="users")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    users = relationship("User", back_populates="property")
