# validators.py-------------------

def check_price(price):
    if price == "":
        return False, "قیمتی وارد نکردید."
    if price.startswith("0"):
        return False, "قیمت نباید با 0 شروع شود."
    if not price.isdigit():
        return False, "قیمت فقط باید عدد باشد."
    if not len(price) > 2:
        return False, "قیمت نباید کمتر از 2 رقم باشد."
    return True, int(price)

def check_identifier(id_num):
    if id_num == "":
        return False, "شناسه وارد نشده است."
    if not id_num.isdigit():
        return False, "شناسه فقط باید عدد و رمز باشد."
    return True, int(id_num)

def check_stock(stock):
    if stock == "":
        return False, "موجودی کالا وارد نشده است."
    if len(stock) < 0:
        return False, "موجودی کالا نباید کمتر از 0 نباشد."
    if not stock.isdigit():
        return False, "موجودی کالا فقط باید عدد باشد."
    return True, int(stock)

def check_name(name):
    if name == "":
        return False ,"نام خالی است."
    if len(name) < 3:
        return False, "نام نباید کمتر از 3 کاراکتر باشد."
    return True , name