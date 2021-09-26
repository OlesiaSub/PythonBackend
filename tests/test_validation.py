import pytest
from app.expense_validation import validator
from app.storage import storage
from model.tracker_model import Expense


def test_validate_id_basic():
    validator.validate_id(2)


def test_validate_id_zero():
    validator.validate_id(0)


@pytest.mark.xfail()
def test_validate_id_negative_fail():
    validator.validate_id(-2)


@pytest.mark.xfail()
def test_validate_name_numeric_fail():
    validator.validate_name("5564")


@pytest.mark.xfail()
def test_validate_name_empty_fail():
    validator.validate_name("")


@pytest.mark.xfail()
def test_validate_name_lowercase_fail():
    validator.validate_name("hello")


def test_validate_name():
    validator.validate_name("Hello")


def test_available_storage():
    validator.check_available_storage(4)


def test_check_presence_not_present():
    assert not storage.check_presence(1)


def test_check_presence_present():
    expense1 = Expense
    expense1.expense_id = 1
    storage.add_item(expense1)
    assert storage.check_presence(1)
