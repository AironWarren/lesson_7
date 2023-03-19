class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            return self.price * quantity
        else:
            raise ValueError

    def __hash__(self):
        return hash(self.name + self.description)


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
            old_quantity = self.products.get(product)
            self.products[product] = quantity + old_quantity
        else:
            self.products[product] = quantity

        return product.name, self.products[product]

    def remove_product(self, product: Product, quantity=None):
        """
        Метод удаления продукта из корзины.
        Если quantity не передан, то удаляется вся позиция
        Если quantity больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:
            if quantity is None or quantity >= self.products.get(product):
                del self.products[product]
                return 'Продукт полностью удален из корзины'
            else:
                old_quantity = self.products.get(product)
                self.products[product] = old_quantity - quantity
        else:
            raise AttributeError

        return product.name, self.products[product]

    def clear(self):
        return 'Корзина очищена', self.products.clear()

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
        dict_p = {
            'total volume': 0
        }
        for key in self.products:
            if self.products[key] > key.quantity:
                dict_p.clear()
                raise ValueError
            else:
                dict_p['total volume'] += self.products[key]
                dict_p[key.name] = self.products[key]

        return dict_p
