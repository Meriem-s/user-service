from webbrowser import get
from fastapi import FastAPI, Path, Query, HTTPException, status, Depends
from app.database import SessionLocal
from app import models
import app.schemas as schemas
from app.database import Base, engine
from sqlalchemy.orm import Session
from . import helper
from email_validator import validate_email, EmailNotValidError

app = FastAPI()
Base.metadata.create_all(bind=engine)

print("###### Creating DB Table ######")
try:
    Base.metadata.create_all(bind=engine)
except:
    print("table already exists")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", status_code=status.HTTP_200_OK)
async def get_user(
    name: str = Query(
        None, description="The name of the user you'd like to view", min_length=1
    ),
    user_id: int = Query(
        None, description="The id of the user you'd like to view", gt=0
    ),
    db: Session = Depends(get_db),
):
    if user_id and not name:
        user = helper.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        emails = helper.get_user_emails_by_id(db, user_id)
        phonenumbers = helper.get_user_phone_numbers(db, user_id)
        output_user = schemas.User(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            emails=emails,
            phonenumbers=phonenumbers,
        )

        return output_user

    elif name and not user_id:
        users = helper.get_user_by_name(db, name=name)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        output_users = []
        for user in users:
            emails = helper.get_user_emails_by_id(db, user_id=user.id)
            phonenumbers = helper.get_user_phone_numbers(db, user_id=user.id)
            output_user = schemas.User(
                id=user.id,
                firstname=user.firstname,
                lastname=user.lastname,
                emails=emails,
                phonenumbers=phonenumbers,
            )
            output_users.append(output_user)

        if len(users) == 1:
            return output_users[0]
        elif len(users) > 1:
            return output_users

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Query by id OR by name"
        )


@app.post("/create-user/", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(firstname=user.firstname, lastname=user.lastname)
    email = helper.get_user_emails_by_email(db, user.mail)
    phoneNumber = helper.get_user_phone(db, user.phoneNumber)

    # validate email format
    try:
        email_valid = validate_email(user.mail).email
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Email format"
        )

    # check if email has been already used
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email has been already used by another user",
        )

    if phoneNumber != None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number has been already used by another user",
        )
    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # get user_id
        user_id_db = new_user.id
        new_email = models.Email(mail=user.mail, user_id=user_id_db)
        new_phone = models.PhoneNumber(number=user.phoneNumber, user_id=user_id_db)
        db.add(new_email)
        db.add(new_phone)
        db.commit()

        return new_user


@app.delete("/delete-user/{user_id}")
async def delete_item(
    user_id: int = Query(..., description="The ID of the user to delete", gt=0),
    db: Session = Depends(get_db),
):
    user_to_delete = helper.get_user_by_id(db, user_id)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User ID does not exist so cannot be deleted",
        )

    db.delete(user_to_delete)
    db.commit()


@app.put("/add-data/{user_id}", status_code=status.HTTP_200_OK)
async def add_data(user_id: int, data: schemas.DataAdd, db: Session = Depends(get_db)):
    # validate emails format
    if data.mail != None:
        try:
            email_valid = validate_email(data.mail).email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Email format"
            )

        email_to_add = (
            db.query(models.Email).filter(models.Email.mail == data.mail).first()
        )
        if email_to_add:  # if email exists then cannot add it to DB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        new_email = models.Email(mail=data.mail, user_id=user_id)
        db.add(new_email)
        db.commit()
        db.refresh(new_email)

    if data.number != None:
        number_to_add = (
            db.query(models.PhoneNumber)
            .filter(models.PhoneNumber.number == data.number)
            .first()
        )
        if number_to_add:  # if number exists then cannot add it to DB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number already exists",
            )
        new_number = models.PhoneNumber(number=data.number, user_id=user_id)
        db.add(new_number)
        db.commit()
        db.refresh(new_email)

    updated_user = helper.get_user_by_id(db, user_id)
    return updated_user


@app.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_mail(
    user_id: int, data: schemas.DataUpdate, db: Session = Depends(get_db)
):

    if data.old_mail != None and data.new_mail != None:
        email_to_update = helper.get_email_by_id_and_mail(db, user_id, data.old_mail)

        if not email_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Email does not exist"
            )

        # validate emails format
        try:
            email_valid = validate_email(data.new_mail).email
            email_valid = validate_email(data.old_mail).email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Email format"
            )

        try:
            email_to_update.mail = data.new_mail
            db.commit()

        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cannot update email"
            )

    if data.old_number != None and data.new_number != None:
        number_to_update = helper.get_number_by_id_and_number(
            db, user_id, data.old_number
        )
        if not number_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Number does not exist",
            )

        else:
            try:
                number_to_update.number = data.new_number
                db.commit()

            except:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Cannot update Number"
                )

    if (data.old_number == None or data.new_number == None) and (
        data.old_mail == None or data.new_mail == None
    ):
        return {"error": "Check Fields"}

    return {"msg": "Update Sucessfull"}
