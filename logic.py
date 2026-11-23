# logic.py-----------
from storage import load_products
from validators import check_identifier
import csv
def add_product(data, name, price, stock, address):
    ids = [int(key) for key in data]
    new_id = str(max(ids, default=0) + 1)
    data[new_id] = {"name":name, "price":int(price), "stock":int(stock),"address":address}
    return data, ""

def find_product(name_csv):
    try:
        with open("store.csv","r",newline="",encoding="utf-8-sig") as f:
            data = csv.DictReader(f)
            for data_csv in data:
                if data_csv["name"] == name_csv:
                    return True, data_csv
            return False, "در سبد خرید پیدا نشد."
    except FileNotFoundError:
        return False, "سبد خرید خالی است."

def delete_product(identifier):
    try:
        data = load_products()
        bool_1 ,corrected = check_identifier(identifier)
        if not bool_1:
            return False, corrected
        data.pop(str(corrected))
        return True, data
    except KeyError as e:
        return False, f" پبدا نشد: {e} "

def json_stock(products, quantity, stock_new):
    data = load_products()
    if not products in data:
        return False, "شناسه پیدا نشد."
    ids = data[products].get("stock")
    if int(ids) == int(quantity):
        data[products].update({"stock":int(stock_new)})
        return True, data
    else:
        return False, "شناسه اشتباه است."