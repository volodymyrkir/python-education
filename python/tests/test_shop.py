import pytest
from to_test import Product, Shop


@pytest.fixture()
def products_list():
    p1 = Product("Onion", 3)
    p2 = Product("Garlic", 2, 7)
    p3 = Product("Apple", 5, 3)
    return [p1, p2, p3]


@pytest.fixture()
def shop_prepared(products_list):
    return Shop(products_list)


def test_shop_init(shop_prepared):
    assert len(shop_prepared.products) == 3


def test_shop_empty():
    assert len(Shop([]).products) == 0


def test_append_product(shop_prepared):
    new_product = Product("Meat", 100, 3)
    shop_prepared.add_product(new_product)
    assert shop_prepared.products[len(shop_prepared.products) - 1] is new_product


def test_append_smth(shop_prepared):
    new_product = 3
    shop_prepared.add_product(new_product)
    assert shop_prepared.products[len(shop_prepared.products) - 1] is None


def test_empty_list():
    assert Shop().products is None


def test_get_index(shop_prepared):
    assert shop_prepared._get_product_index("Garlic") == 1


@pytest.mark.parametrize("incorrect_input", ("Soup", 1, None))
def test_incorrect_index(shop_prepared, incorrect_input):
    assert shop_prepared._get_product_index(incorrect_input) is None


def test_sell_products(shop_prepared):
    shop_prepared.sell_product("Garlic", 2)
    shop_prepared.sell_product("Onion")
    assert shop_prepared.money == 7.0


def test_sell_all(shop_prepared):  # should raise value error, same as selling more than possible
    shop_prepared.sell_product("Onion")
    with pytest.raises(ValueError):
        shop_prepared.sell_product("Onion")


def test_sell_more(shop_prepared):
    with pytest.raises(ValueError):
        shop_prepared.sell_product("Onion", 3)
