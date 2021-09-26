from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_valid_expense():
    res = client.post("expenses/",
                      json={
                          "name": "Olesya",
                          "expenditure": 100,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": 3
                      })
    assert res.status_code == 200


def test_invalid_id():
    res = client.post("expenses/",
                      json={
                          "name": "Olesya",
                          "expenditure": 100,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": -2
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "Id is invalid, must be >= 0"}


def test_invalid_lowercase_name():
    res = client.post("expenses/",
                      json={
                          "name": "olesya",
                          "expenditure": 34,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": 0
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "Name must start with capital, must not be empty or numeric"}


def test_invalid_numeric_name():
    res = client.post("expenses/",
                      json={
                          "name": "24",
                          "expenditure": 100,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": 1
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "Name must start with capital, must not be empty or numeric"}


def test_invalid_empty_name():
    res = client.post("expenses/",
                      json={
                          "name": "",
                          "expenditure": 400,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": 0
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "Name must start with capital, must not be empty or numeric"}


def test_invalid_is_before_invalid_name():
    res = client.post("expenses/",
                      json={
                          "name": "olesya",
                          "expenditure": 1500,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": -2
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "Id is invalid, must be >= 0"}


def test_item_already_exists():
    client.post("expenses/",
                json={
                    "name": "Olesya",
                    "expenditure": 100,
                    "date": "2021-09-26T07:38:59.388Z",
                    "category": "cat",
                    "description": "description",
                    "expense_id": 2
                })
    res = client.post("expenses/",
                      json={
                          "name": "Polina",
                          "expenditure": 300,
                          "date": "2021-09-26T07:38:59.388Z",
                          "category": "cat",
                          "description": "description",
                          "expense_id": 2
                      })
    assert res.status_code == 400
    assert res.json() == {"detail": "This id already exists"}
