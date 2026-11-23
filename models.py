# models.py-----------
import requests,html
from pathlib import Path

STYLE = """
.card { width: 260px; padding: 12px; border: 1px solid #ccc; border-radius: 12px; }
.card img { width: 100%; border-radius: 8px; }
"""
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

    def can_afford(self, money_user,x):
        if not money_user.isdigit():
            return False, "پول فقط باید عدد باشد."
        if int(money_user) <= 0:
            return False, "پول نباید 0 یا کمتر از آن باشد."
        if self.price > int(money_user):
            return False, "پول شما برای خرید این کالا کافی نیست."
        total = int(self.price) * int(x)
        bool_1 = int(money_user) >= total
        if not bool_1:
            return bool_1, "پول شما برای خرید کافی نیست."
        return bool_1, ""
    def to_data(self):
        data = {"name":self.name, "price":self.price, "stock":self.stock}
        return data

class Data:
    def __init__(self, address):
        self.address = address
    def review(self):
        try:
            if not self.address:
                return False, "ادرس عکس این کالا موجود نیست."
            if not self.address.startswith("https:/"):
                return False, "ادرس باید: {.../:https} شروع شود."
            r = requests.get(url=self.address,timeout=15)
            r.raise_for_status()
            if len(r.content) > 5 * 1024 * 1024:
                return False, "حجم عکس بیشتر از 5 مگابایت است."
            return True, ""
        except requests.exceptions.HTTPError as e:
            return False, f" خطا: {e.response.status_code}"
        except requests.exceptions.Timeout:
            return False, "زمان تمام شد."
        except requests.exceptions.ConnectionError:
            return False, f" اتصال برقرار نشد. "
        except requests.exceptions.MissingSchema:
            return False, f"ادرس پیدا نشد."
        except requests.exceptions.RequestException:
            return False, "ارتباط برنامه با سایت یا سرور با مشکل مواجه شد."

    def photo(self,image_name,name,price,x):
        try:
            r = requests.get(url=self.address, timeout=15)
            r.raise_for_status()
            data = {"image/jpeg": "jpg", "image/png": "png"}
            con = r.headers.get("Content-Type","").split(";")[0]
            new = data.get(con)
            if new is None:
                return False, "آدرس داده شده عکس نیست."
            folder = Path("images")
            folder.mkdir(exist_ok=True)
            path = folder / f"{image_name}"
            with open(path,"wb") as f:
               f.write(r.content)
               return True, f"""<!DOCTYPE html>
               <html lang="fa" dir="rtl">
               <head>
               <meta charset="utf-8">
               <title>{html.escape(name)}</title>
               <style>{STYLE}</style>
               </head>
               <body>
               <div class="card">
               <img src="{path}" alt="">
               <h2>{html.escape(name)}</h2>
               <p>قیمت: {price:,}</p>
               <p>تعداد: {x}</p>
               </div>
               </body>
               </html>"""
        except requests.exceptions.HTTPError as e:
            return False, f" خطا: {e.response.status_code}"
        except requests.exceptions.Timeout:
            return False, "زمان تمام شد."
        except requests.exceptions.ConnectionError:
            return False, f" اتصال برقرار نشد. "
        except requests.exceptions.RequestException:
            return False, "ارتباط برنامه با سایت یا سرور با مشکل مواجه شد."