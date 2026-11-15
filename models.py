# models.py-----------
class Product:
    def __init__(self,name:str,price:int,stock:int):
        self.stock = stock
        self.price = price
        self.name = name

    def sell(self, quantity):
        if not quantity.isdigit():
            return False, "تعداد فقط باید عدد باشد."
        if int(quantity) <= 0:
            return False, "تعداد باید بیشتر از صفر باشد."
        if int(quantity) > self.stock:
            return False, "موجودی کالا کافی نیست."
        if int(quantity) == self.stock:
            self.stock = 0
            return True, "فروخته شد."
        self.stock -= int(quantity)
        return True, "فروخته شد."

    def can_afford(self, money_user):
        if not money_user.isdigit():
            return False, "پول فقط باید عدد باشد."
        if int(money_user) <= 0:
            return False, "پول نباید 0 یا کمتر از آن باشد."
        if self.price > int(money_user):
            return False, "پول شما برای خرید این کالا کافی نیست."
        return True, ""

    def to_data(self):
        data = {"name":self.name, "price":self.price, "stock":self.stock}
        return data