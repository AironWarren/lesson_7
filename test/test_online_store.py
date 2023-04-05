"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models.store_products import Product
from models.user_shopping_cart import Cart


@pytest.fixture()
def books():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture()
def copybooks():
    return Product("copybook", 50, "This is a copybook", 10000)


@pytest.fixture()
def pens():
    return Product("pen", 20, "This is a pen", 20000)


@pytest.fixture()
def pencils():
    return Product("pencil", 10, "This is a pencil", 20000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, books):
        # TODO напишите проверки на метод check_quantity
        assert books.check_quantity(500)
        assert books.check_quantity(books.quantity)
        assert not books.check_quantity(2000)

        with pytest.raises(ValueError):
            assert books.check_quantity(0) is ValueError

    def test_product_buy(self, books):
        # TODO напишите проверки на метод buy
        books.buy(200)
        assert 800 == books.quantity
        books.buy(books.quantity)
        assert 0 == books.quantity

    def test_product_buy_more_than_available(self, books):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert books.buy(2000) is ValueError


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, copybooks, pens):
        cart = Cart()
        cart.add_product(copybooks, 6)
        assert cart.products[copybooks] == 6
        cart.add_product(copybooks, 5)
        assert cart.products[copybooks] == 11
        cart.add_product(pens)
        assert cart.products[pens] == 1

    def test_negative_add_product(self, copybooks):
        cart = Cart()

        with pytest.raises(ValueError):
            assert cart.add_product(copybooks, 0) is ValueError

    def test_remove_product(self, copybooks, pens, pencils):
        cart = Cart()

        cart.add_product(copybooks, 6)
        cart.add_product(copybooks, 5)
        cart.add_product(pencils, 35)

        cart.remove_product(copybooks, 5)
        assert cart.products[copybooks] == 6

        cart.remove_product(pencils)
        assert pencils not in cart.products.keys()

        cart.add_product(pencils, 10)
        cart.remove_product(pencils, 15)
        assert pencils not in cart.products.keys()

        with pytest.raises(LookupError):
            assert cart.remove_product(pens) is LookupError

    def test_clear_cart(self, copybooks, pencils):
        cart = Cart()

        cart.add_product(copybooks, 6)
        cart.add_product(copybooks, 5)
        cart.add_product(pencils, 35)

        cart.clear()

        assert cart.products == {}

    def test_get_total_price(self, copybooks, pens, pencils):
        cart = Cart()

        cart.add_product(copybooks, 500)
        cart.add_product(pens, 800)
        cart.add_product(pencils, 5000)

        assert cart.get_total_price() == (copybooks.price * 500 + pens.price * 800 + pencils.price * 5000)

    def test_buy(self, copybooks, pens, pencils):
        cart = Cart()

        cart.add_product(copybooks, 500)
        cart.add_product(pens, 800)
        cart.add_product(pencils, 5000)

        cart.buy()

        assert copybooks.quantity == (10000 - 500) and pens.quantity == (20000 - 800) and pencils.quantity == (
                20000 - 5000)

    def test_negative_buy(self, copybooks, pens, pencils):
        cart = Cart()

        cart.add_product(copybooks, 10001)
        cart.add_product(pens, 800)
        cart.add_product(pencils, 5000)

        with pytest.raises(ValueError):
            assert cart.buy() is ValueError

    def test_product_information(self, copybooks):
        assert copybooks.description == "This is a copybook"
