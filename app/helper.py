from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_emails_by_id(db: Session, user_id: int):
    return db.query(models.Email).filter(models.Email.user_id == user_id).all()


def get_user_emails_by_email(db: Session, mail: str):
    return db.query(models.Email).filter(models.Email.mail == mail).all()


def get_user_phone_numbers(db: Session, user_id: int):
    phone_numbers = (
        db.query(models.PhoneNumber).filter(models.PhoneNumber.user_id == user_id).all()
    )
    return phone_numbers


def get_user_phone(db: Session, number: str):
    return (
        db.query(models.PhoneNumber).filter(models.PhoneNumber.number == number).first()
    )


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.firstname == name).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_email_by_id_and_mail(db: Session, user_id: int, mail: str):
    return (
        db.query(models.Email)
        .filter(and_(models.Email.user_id == user_id, models.Email.mail == mail))
        .first()
    )


def get_number_by_id_and_number(db: Session, user_id: str, number: str):
    return (
        db.query(models.PhoneNumber)
        .filter(
            and_(
                models.PhoneNumber.user_id == user_id,
                models.PhoneNumber.number == number,
            )
        )
        .first()
    )
