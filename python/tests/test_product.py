import pytest
from to_test import Product


@pytest.fixture()
def product_onion():
    return Product("Onion", 3, 4)


@pytest.fixture()
def product_onion_incorrect():
    return Product("Onion", -10, -4)


def test_init_default():
    assert Product("Melon", 10).quantity == 1


def test_init_negativeprice(product_onion_incorrect):
    assert product_onion_incorrect.price == 0


def test_init_negativequantity(product_onion_incorrect):
    assert product_onion_incorrect.quantity == 1


def test_subtract_quantity(product_onion):
    product_onion.subtract_quantity(2)
    assert product_onion.quantity == 2


def test_add_quantity(product_onion):
    product_onion.add_quantity(5)
    assert product_onion.quantity == 9


def test_change_price(product_onion):
    product_onion.change_price(30)
    assert product_onion.price == 30


def test_change_incorrectprice(product_onion):
    product_onion.change_price(-10)
    assert product_onion.price == 0
