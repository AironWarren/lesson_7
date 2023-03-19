"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models.auxiliary_classes import Product, Cart


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
        assert product.check_quantity(
            500), "Количество запрашиваемого продукта больше существующих объемов"

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.price * 500 == product.buy(500)

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
        assert cart.add_product(copybook, 6) == (copybook.name, 6)
        assert cart.add_product(copybook, 5) == (copybook.name, 11)
        assert cart.add_product(pen) == (pen.name, 1)

    def test_negative_add_product(self, copybook, pen, pencil):
        cart = Cart()

        with pytest.raises(ValueError):
            assert cart.add_product(copybook, 0) is ValueError

    def test_remove_product(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 6)
        cart.add_product(copybook, 5)
        cart.add_product(pencil, 35)

        assert cart.remove_product(copybook, 5) == (copybook.name, 6)
        assert cart.remove_product(pencil) == 'Продукт полностью удален из корзины'
        cart.add_product(pencil, 10)
        assert cart.remove_product(pencil, 15) == 'Продукт полностью удален из корзины'

        with pytest.raises(AttributeError):
            assert cart.remove_product(pen) is AttributeError

    def test_clear_basket(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 6)
        cart.add_product(copybook, 5)
        cart.add_product(pencil, 35)

        assert cart.clear() == ('Корзина очищена', None)

    def test_get_total_price(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 500)
        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        assert cart.get_total_price() == (copybook.price * 500 + pen.price * 800 + pencil.price * 5000)

    def test_buy(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 500)
        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        assert cart.buy() == {'total volume': 6300, 'copybook': 500, 'pen': 800, 'pencil': 5000}

    def test_negative_buy(self, copybook, pen, pencil):
        cart = Cart()

        cart.add_product(copybook, 10001)
        cart.add_product(pen, 800)
        cart.add_product(pencil, 5000)

        with pytest.raises(ValueError):
            assert cart.buy() is ValueError
