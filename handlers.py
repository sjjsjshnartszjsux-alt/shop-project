# handlers.py--------------------
from validators import check_price,check_identifier,check_stock,check_name
from storage import load_products,save_products,save_store_csv
from logic import add_product,delete_product,json_stock,find_product
from models import Product
from api import Internet,Ticket
import csv

def store_option_1(data):
    print("برای بازگشت 4 را وارد کنید.")
    name = input("نام کالا: ").strip()
    if name == "4":
        return
    else:
        bool_1, name_end = check_name(name)
        if not bool_1 == True:
            print(name_end,"\n")
            store_option_1(load_products())
            return
        price = input("قیمت کالا: ").strip()
        bool_1 , price_end = check_price(price)
        if not bool_1 == True:
            print(price_end)
            store_option_1(load_products())
            return
        stock_commodity = input("موجودی کالا: ").strip()
        bool_3, stock_commodity_end = check_stock(stock_commodity)
        if not bool_3 == True:
            print(stock_commodity_end)
            store_option_1(load_products())
            return
        data_1, str_1 = add_product(data,name_end,price,stock_commodity_end)
        if str_1 == "":
            save_products(data_1)
            print("در انبار ذخیره شد.","\n")
            return
        else:
            print(str_1,"\n")
            return

def store_option_2():
    data = load_products()
    if not data:
        print("{}")
    else:
        for key in data.items():
            print(key ,"\n")

def store_option_3():
    print("برای بازگشت 4 وارد کنید.")
    identifier = input("شناسه کالا خود را وارد کنید: ").strip()
    if identifier == "4":
        return
    bool_1, data_end = delete_product(identifier)
    if not bool_1 == True:
        print(data_end)
        return
    else:
        save_products(data_end)
        print("کالا در انبار با این شناسه حذف شد.", "\n")
        return
def store_option_4():
    dic = {}
    print("برای بازگشت 0 را وارد کنید.")
    identifier = input("شناسه کالا: ").strip()
    if identifier == "0":
        return
    bool_1 , identifier_end = check_identifier(identifier)
    if not bool_1:
        print(identifier_end)
        return
    for ro, data in load_products().items():
        dic = data
        if int(ro) == int(identifier_end):
            break
    quantity = input("تعداد الان کالا: ").strip()
    for a,row in load_products().items():
        if str(row["stock"]) == quantity:
            stock = input("تعداد جدید کالا: ").strip()
            bool_4 ,stock_end = check_stock(stock)
            if not bool_4:
                print(stock_end)
                return
            bool_3, data_stock = json_stock(identifier,quantity,stock_end)
            if not bool_3:
                print(data_stock)
                return
            save_products(data_stock)
            print("موجودی این کالا ذخیره شد." ,"\n")
    if not str(dic.get("stock")) == str(quantity):
        print("تعداد الان کالا صحیح نیست.","\n")
        return
def store_option_6():
    store_option_2()
    lis = {}
    print("\n برای بازگشت 4 وارد کنید.")
    name = input("نام کالا: ").strip()
    if name == "4":
        return
    bool_1, new_name = check_name(name)
    if not bool_1:
        print(new_name,"\n")
        return
    data_json = load_products()
    if data_json == {}:
        print("سبد خرید خالی است.","\n")
        return
    for ro, data_new in data_json.items():
        lis = data_new
    for a,data in data_json.items():
        if data["name"] == new_name:
            d = Product(**data)
            quantity = input("تعداد کالای که می خواهید: ").strip()
            bool_2, text_num = d.sell(quantity)
            if not bool_2:
                print(text_num,"\n")
                return
            pol = input("پول شما چقدر است: ").strip()
            bool_3, pol_2 = d.can_afford(pol)
            if not pol_2 == "":
                print(pol_2, "\n")
                return
            ti = Ticket(data["price"])
            if not pol.isdigit():
                print("فقط برای پول عدد وارد کنید.")
                return
            bool_4 = ti.can_buy(pol,quantity)
            if not bool_4:
                print(bool_4, "پول شما برای خرید این تعداد کافی نیست.")
                return
            data_csv = d.to_data()
            new_json = data_csv.pop("stock")
            data_csv["id"] = int(a)
            data_csv["number"] = int(quantity)
            save_store_csv(data_csv)
            print(text_num)
            new_data = load_products()
            if int(d.stock) == 0:
                new_data.pop(str(a))
                save_products(new_data)
                print("\n")
                return
            else:
                new_data[str(a)]["stock"] = new_json
                save_products(new_data)
                print("\n")
                return
    for row in lis:
        if str(new_name) == row["name"]:
            pass
        else:
            print("پیدا نشد.", "\n")
            return
def store_option_7():
    print("برای بازگشت 4 وارد کنید.")
    name = input("نام کالا: ").strip()
    if name == "4":
        return
    bol_1,name_new = check_name(name)
    if not bol_1 == True:
        print(name_new,"\n")
        store_option_7()
        return
    try:
        with open("store.csv", "r", newline="", encoding="utf-8-sig") as f:
            memory = list(csv.DictReader(f))
            with open("store.csv", "w", newline="", encoding="utf-8-sig") as new_file:
                wri = csv.DictWriter(new_file,fieldnames=["name","price","id","number"])
                wri.writeheader()
                for row in memory:
                    if row["name"] != name_new:
                        wri.writerow(row)
                with open("store.csv", "r", newline="", encoding="utf-8-sig") as file:
                    memory_2 = list(csv.DictReader(f))
                if not name_new in memory_2:
                    print(f" ردیف با نام {name_new} حذف شد. ")
                else:
                    print("حذف نشد.")
    except FileNotFoundError:
        print("هنوز کالای خرید نکردید.")
    except KeyError as e:
        print(f" پیدا نشد.{e}نام:")
def store_option_8():
    confirm = input("برای پاک کردن انبار تایید کنید.").strip()
    if confirm == "تایید":
        with open("products.json", "w", encoding="utf-8"):
            print("انبار پاک شد.", "\n")
    else:
        print("حذف نشد.", "\n")
def store_option_9():
    try:
        with open("store.csv", "r", newline="" ,encoding="utf-8-sig") as f:
            data_csv = csv.DictReader(f)
            if not data_csv:
                print("هنور کالای خرید نکردید.")
            else:
                for a in data_csv:
                    print(a, "\n")
    except FileNotFoundError:
        print("{}","\n")

def store_option_10():
    data_json = load_products()
    print("برای خروج 0 را وارد کنید.")
    name_csv = input("نام کالا خریداری شده: ").strip()
    if name_csv == "0":
        return
    bool_2, new_name_csv = check_name(name_csv)
    if not bool_2:
        print(new_name_csv)
        return
    bool_3, json_pc_2 = find_product(new_name_csv)
    for key,json_pc_1 in data_json.items():
        if json_pc_1.get("name") == new_name_csv:
            print(f" سبد خرید: {json_pc_1} ","\n")
        else:
            print("پیدا نشد.")
        if not bool_3:
            print(json_pc_2,"\n")
        else:
            print(f" لیست خریداری شده: {json_pc_2}", "\n")
def store_option_11():
    print("برای خروج 0 وارد کنید.","\n :ما در سایت ",
          "https://jsonplaceholder.typicode.com/posts","\n "
           "اطلاعت شما را پیدا می کنیم.")
    uses_new = input("کاربر شماره چند هستید: ").strip()
    if uses_new == "0":
        return
    id_user = input("ایدی شما چند است: ").strip()
    d = Internet("https://jsonplaceholder.typicode.com/posts",uses_new,id_user,"","")
    bool_1, str_1 = d.check_user(uses_new)
    if not bool_1:
        print(str_1,"\n")
        return
    bool_2, str_2 = d.check_id(id_user)
    if not bool_2:
        print(str_2)
        return
    bool_3, str_3 = d.search_internet()
    if not bool_3:
        print(str_3)
        return
    print(str_3 , "\n")

def store_option_12():
    print("برای خروج 0 وارد کنید.")
    user_name = input("کاربر شماره چند هستید: ").strip()
    if user_name == "0":
        return
    d = Internet("https://jsonplaceholder.typicode.com/posts","","","","")
    bool_1, str_1 = d.check_user(user_name)
    if not str_1 == "":
        print(str_1, "\n")
        return
    title_1 = input("متن اول نام مشخصات را وارد کنید: ")
    bool_2, str_2 = d.chock_title(title_1)
    if not bool_2:
        print(str_2, "\n")
        return
    print(str_2, "\n")
    body_1 = input("متن دوم توضیح خود را وارد کنید: ")
    bool_3, str_3 = d.chock_body(body_1)
    if not bool_3:
        print(str_3, "\n")
        return
    print(str_3, "\n")
    bool_data, key = d.create_post(title_1,body_1,user_name)
    if not bool_data:
        print(key, "\n")
        return
    print(f" ذخیره شد: {bool_data}", "\n",f"{key}\n")

def store_option_13():
    print("برای خروج 0 وارد کنید.")
    data = input("برای نمایش تمام داده ها تایید کنید: ").strip()
    if data == "0":
        return
    if data == "تایید" or data == "اره":
        d = Internet("https://jsonplaceholder.typicode.com/posts", "", "", "", "")
        data_new, address, json_new = d.to_data()
        if not json_new:
            print(address, "\n")
        else:
            print(json_new, "\n")
        if not data_new:
            print(address, "\n")
        else:
            print(data_new, "\n")
        if not address == "[]":
            print(address, "\n")