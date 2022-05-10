from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
import app.database as db


class User(db.Base):
    """
    SQL Schema:
    id INTEGER PRIMARY KEY,
    lastname STRING NOT NULL,
    firstname STRING NOT NULL
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(120), nullable=False)
    firstname = Column(String(120), nullable=False)
    emails = relationship(
        "Email", back_populates="user", cascade="all,delete", passive_deletes=True
    )
    phonenumbers = relationship(
        "PhoneNumber", back_populates="user", cascade="all,delete", passive_deletes=True
    )


class Email(db.Base):
    """SQL Schema:
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mail STRING NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id)
    """

    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    mail = Column(EmailType, unique=True, index=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="emails")


class PhoneNumber(db.Base):
    """SQL Schema:
    id INTEGER PRIMARY KEY,
    number STRING NOT NULL UNIQUE,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id)
    """

    __tablename__ = "phonenumbers"
    id = Column(Integer, primary_key=True)
    number = Column(String(120), unique=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="phonenumbers")
