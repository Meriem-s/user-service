from fastapi.testclient import TestClient
from app.main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base


SQLACLCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@db/perseus_db"
)

engine = create_engine(SQLACLCHEMY_DATABASE_URL, echo=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


data_to_create = {
    "firstname": "meriem",
    "lastname": "said",
    "mail": "test_email@gmail.com",
    "phoneNumber": "123456",
}

test_name = data_to_create["firstname"]


def test_create_user():
    response = client.post("/create-user/", json=data_to_create)
    assert response.status_code == 200

    data = response.json()
    assert data["firstname"] == data_to_create["firstname"]
    assert data["lastname"] == data_to_create["lastname"]
    assert "id" in data
    assert "emails" in data
    assert "phonenumbers" in data

def test_get_user():
    response = client.get("/users?name={test_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == data_to_create["fistname"]
    assert "id" in data["emails"]
    assert "id" in data["phonenumbers"]
    assert data["emails"] == data_to_create["mail"]
    assert data["phonenumbers"]["phoneNumber"] == data_to_create["phoneNumber"]
    # test get user data by id
    user_id = data["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["firstname"] == data_to_create["fistname"]
    assert data["emails"] == data_to_create["mail"]
    assert data["phonenumbers"]["phoneNumber"] == data_to_create["phoneNumber"]


def test_read_inexistent_user():
    response = client.get("/users?name=inexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_create_existing_user_email():
    response = client.post(
        "/create-user/",
        json={data_to_create},
    )
    print(response.json())
    assert response.status_code == 400
    assert response.json() == {"detail": "Email has been already used by another user"}


def test_create_existing_user_phone():
    response = client.post(
        "/create-user/",
        json={
            "firstname": "meriem",
            "lastname": "said",
            "email": "test_email_2@gmail.com",
            "phonenumber": "123456",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Phone number has been already used by another user"
    }
