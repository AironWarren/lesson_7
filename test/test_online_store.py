"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models.store_products import Product
from models.user_shopping_cart import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture()
def copybook():
    return Product("copybook", 50, "This is a copybook", 10000)


@pytest.fixture()
def pen():
    return Product("pen", 20, "This is a pen", 20000)


@pytest.fixture()
def pencil():
    return Product("pencil", 10, "This is a pencil", 20000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(500)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(200)
        assert 800 == product.quantity

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert product.buy(1001) is ValueError


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, copybook, pen, pencil):
        cart = Cart()
        cart.add_product(copybook, 6)
        assert cart.products[copybook] == 6
        cart.add_product(copybook, 5)
        assert cart.products[copybook] == 11
        cart.add_product(pen)
        assert cart.products[pen] == 1

    def test_negative_add_product(self, copybook, pen, pencil):
        cart = Cart()

        with pytest.raises(ValueError):
            assert cart.add_product(copybook, 0) is ValueError

        with pytest.raises(ValueError):
            assert cart.add_product(copybook, 10001) is ValueError

    def test_remove_product(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 6)
        cart.add_product(copybook, 5)
        cart.add_product(pencil, 35)

        cart.remove_product(copybook, 5)
        assert cart.products[copybook] == 6

        cart.remove_product(pencil)
        assert pencil not in cart.products.keys()

        cart.add_product(pencil, 10)
        cart.remove_product(pencil, 15)
        assert pencil not in cart.products.keys()

        with pytest.raises(AttributeError):
            assert cart.remove_product(pen) is AttributeError

    def test_clear_basket(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 6)
        cart.add_product(copybook, 5)
        cart.add_product(pencil, 35)

        cart.clear()

        assert cart.products == {}

    def test_get_total_price(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 500)
        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        assert cart.get_total_price() == (copybook.price * 500 + pen.price * 800 + pencil.price * 5000)

    def test_negative_total_price(self, copybook, pen, pencil):
        cart = Cart()

        try:
            cart.add_product(copybook, 10001)
        except ValueError:
            pass

        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        with pytest.raises(AssertionError):
            assert cart.get_total_price() == (copybook.price * 10001 + pen.price * 800 + pencil.price * 5000)

    def test_buy(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 500)
        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        cart.buy()

        assert copybook.quantity == (10000 - 500) and pen.quantity == (20000 - 800) and pencil.quantity == (
                20000 - 5000)

    def test_negative_buy(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 10001)
        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        with pytest.raises(ValueError):
            assert cart.buy() is ValueError

    def test_product_information(self, copybook):
        assert copybook.description == "This is a copybook"

