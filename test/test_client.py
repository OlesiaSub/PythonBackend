import pytest
from fastapi.testclient import TestClient

from main import app
from storage import storage

# уже не актуальны из-за подключения бд

client = TestClient(app)


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 1


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 0


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 0


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 0


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 0


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 0


@pytest.mark.skip(reason="currently unavailable for testing")
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
    assert len(storage.expense_storage) == 1
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
    assert len(storage.expense_storage) == 1


@pytest.mark.skip(reason="currently unavailable for testing")
def test_get_item():
    client.post("expenses/",
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
    assert len(storage.expense_storage) == 1


@pytest.mark.skip(reason="currently unavailable for testing")
def test_get_item_fails():
    client.post("expenses/",
                json={
                    "name": "Expense1",
                    "expenditure": 100,
                    "date": "2021-09-27T01:25:53.857135",
                    "category": "cat",
                    "description": "desc",
                    "expense_id": -2
                })
    res = client.get("/expenses_tracker/1")
    assert res.status_code == 400


@pytest.mark.skip(reason="currently unavailable for testing")
def test_add_multiple_queries():
    for i in range(0, 50):
        client.post("expenses/",
                    json={
                        "name": "Expense1",
                        "expenditure": 100,
                        "date": "2021-09-27T01:25:53.857135",
                        "category": "cat",
                        "description": "desc",
                        "expense_id": i
                    })
    assert len(storage.expense_storage) == 50


@pytest.mark.skip(reason="currently unavailable for testing")
def test_add_and_get_multiple_queries():
    for i in range(0, 50):
        client.post("expenses/",
                    json={
                        "name": "Expense1",
                        "expenditure": 100,
                        "date": "2021-09-27T01:25:53.857135",
                        "category": "cat",
                        "description": "desc",
                        "expense_id": i
                    })
    for i in range(0, 50):
        res = client.get("/expenses_tracker/" + str(i))
        assert res.status_code == 200


@pytest.mark.skip(reason="currently unavailable for testing")
def test_add_with_bad_ids():
    for i in range(-10, 50):
        client.post("expenses/",
                    json={
                        "name": "Expense1",
                        "expenditure": 100,
                        "date": "2021-09-27T01:25:53.857135",
                        "category": "cat",
                        "description": "desc",
                        "expense_id": i
                    })
    assert len(storage.expense_storage) == 50


@pytest.mark.skip(reason="currently unavailable for testing")
def test_add_and_get_with_wrong_ids():
    for i in range(-10, 50):
        client.post("expenses/",
                    json={
                        "name": "Expense1",
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
