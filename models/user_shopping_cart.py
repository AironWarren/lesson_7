from models.store_products import Product


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, quantity=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if quantity == 0:
            raise ValueError

        if product in self.products:
            self.products[product] = quantity + self.products.get(product)
        else:
            self.products[product] = quantity

    def remove_product(self, product: Product, quantity=None):
        """
        Метод удаления продукта из корзины.
        Если quantity не передан, то удаляется вся позиция
        Если quantity больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:
            if quantity is None or quantity >= self.products.get(product):
                del self.products[product]
            else:
                old_quantity = self.products.get(product)
                self.products[product] = old_quantity - quantity
        else:
            raise LookupError

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        get_total = 0
        for key in self.products:
            get_total += key.price * self.products[key]

        return get_total

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for key, values in self.products.items():
            if key.quantity >= values:
                key.quantity = key.quantity - values
            else:
                raise ValueError
