import pytest
from fastapi import HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import db_models
from database.database import Base
from endpoints.endpoints import get_db
from use_case.endpoints_logic import process_get_expense, process_create_expense
from main import app
from model.tracker_model import Expense

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db_tests():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def clear():
    db = TestingSessionLocal()
    try:
        db.query(db_models.Expense).delete()
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db] = get_db_tests
client = TestClient(app)


def test_invalid_id():
    clear()
    with pytest.raises(HTTPException) as execinfo:
        process_get_expense(-1, Depends(get_db))
    assert execinfo.value.status_code == 400
    assert execinfo.value.detail == "Id is invalid, must be >= 0"


def test_invalid_lowercase_name():
    clear()
    ex = Expense(name="olesya", expenditure=30, date="2021-09-26T07:38:59.388Z",
                 category="ff", description="ss", expense_id=1)
    with pytest.raises(HTTPException) as execinfo:
        process_create_expense(ex, Depends(get_db()))
    assert execinfo.value.status_code == 400
    assert execinfo.value.detail == "Name must start with capital, must not be empty or numeric"


def test_item_already_exists():
    clear()
    client.post("expenses/new_expense",
                json={
                    "name": "Olesya",
                    "expenditure": 100,
                    "date": "2021-09-26T07:38:59.388Z",
                    "category": "cat",
                    "description": "description",
                    "expense_id": 2
                })
    res = client.post("expenses/new_expense",
                      json={
                          "name": "Polina",
                          "expenditure": 300,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": 2
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "Expense with this id is already registered"}


def test_get_item():
    clear()
    client.post("expenses/new_expense",
                json={
                    "name": "Expense1",
                    "expenditure": 100,
                    "date": "2021-09-27T01:25:53.857135",
                    "category": "cat",
                    "description": "desc",
                    "expense_id": 1
                })
    res = client.get("/expenses_tracker/1")
    assert res.status_code == 200


def test_add_and_get_multiple_queries():
    clear()
    for i in range(0, 50):
        client.post("expenses/new_expense",
                    json={
                        "name": "Expense" + str(i),
                        "expenditure": 100,
                        "date": "2021-09-27T01:25:53.857135",
                        "category": "cat",
                        "description": "desc",
                        "expense_id": i
                    })
    for i in range(0, 50):
        res = client.get("/expenses_tracker/" + str(i))
        assert res.status_code == 200


def test_add_and_get_with_wrong_ids():
    clear()
    for i in range(-10, 50):
        client.post("expenses/new_expense",
                    json={
                        "name": "Expense" + str(i),
                        "expenditure": 100,
                        "date": "2021-09-27T01:25:53.857135",
                        "category": "cat",
                        "description": "desc",
                        "expense_id": i
                    })
    for i in range(-10, 0):
        res = client.get("/expenses_tracker/" + str(i))
        assert res.status_code == 400

    for i in range(0, 50):
        res = client.get("/expenses_tracker/" + str(i))
        assert res.status_code == 200
