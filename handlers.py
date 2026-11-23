# handlers.py--------------------
from validators import check_price,check_identifier,check_stock,check_name,address_new
from storage import load_products,save_products,save_store_csv
from logic import add_product,delete_product,json_stock,find_product
from models import Product,Data
from pathlib import Path
import csv,webbrowser,requests,json

def store_option_1(data):
    print("برای بازگشت 0 را وارد کنید.")
    name = input("نام کالا: ").strip()
    if name == "0":
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
        new = input("برای گذاشتن عکس برای کالا تایید کنید.").strip()
        if new == "تایید" or new == "اره":
            address = input("ادرس سایت عکس: ").strip()
            ok_2,mass_2 = address_new(address)
            if not ok_2:
                print(mass_2)
                return
            d = Data(address)
            ok, mass = d.review()
            if not ok:
                print(mass)
                return
            data_1, str_1 = add_product(data, name_end, price, stock_commodity_end, address)
            if str_1 == "":
                save_products(data_1)
                print("در انبار ذخیره شد.","\n")
                return
            else:
                print(str_1,"\n")
                return
        else:
            num = input("بدون عکس ذخیره شود؟ (بله/خیر)").strip()
            if num == "بله" or num == "اره":
                data_1, str_1 = add_product(data, name_end, price, stock_commodity_end, "")
                if str_1 == "":
                    save_products(data_1)
                    print("در انبار با اطلاعات ذخیره شد.","\n")
                    return
                else:
                    print(str_1,"\n")
                    return
            else:
                print("ذخیره نشد.")
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
    print("برای بازگشت 0 را وارد کنید.")
    identifier = input("شناسه کالا: ").strip()
    if identifier == "0":
        return
    bool_1 , identifier_end = check_identifier(identifier)
    if not bool_1:
        print(identifier_end)
        return
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
            return
    print("تعداد الان کالا صحیح نیست.","\n")
    return
def store_option_6():
    store_option_2()
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
    for a,data in data_json.items():
        if data["name"] == new_name:
            new_dic = data.pop("address","")
            d = Product(**data)
            quantity = input("تعداد کالای که می خواهید: ").strip()
            bool_2, text_num = d.sell(quantity)
            if not bool_2:
                print(text_num,"\n")
                return
            pol = input("پول شما چقدر است: ").strip()
            bool_3, pol_2 = d.can_afford(pol,quantity)
            if not bool_3:
                print(pol_2, "\n")
                return
            data_csv = d.to_data()
            new_json = data_csv.pop("stock")
            data_csv["id"] = int(a)
            data_csv["number"] = int(quantity)
            data_csv["address"] = new_dic
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
                new_data[str(a)]["address"] = new_dic
                save_products(new_data)
                print("\n")
                return
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
        return
    try:
        with open("store.csv", "r", newline="", encoding="utf-8-sig") as f:
            memory = list(csv.DictReader(f))
            for row_new in memory:
                if row_new["name"] == name_new:
                    with open("store.csv", "w", newline="", encoding="utf-8-sig") as new_file:
                        wri = csv.DictWriter(new_file,fieldnames=["name","price","id","number","address"])
                        wri.writeheader()
                    for row in memory:
                        if row["name"] != name_new:
                            wri.writerow(row)
                    with open("store.csv", "r", newline="", encoding="utf-8-sig") as file:
                        memory_2 = list(csv.DictReader(file))
                    for new in memory_2:
                        if new["name"] == name_new:
                            print("حذف نشد.")
                            return
                    print(f" ردیف با نام {name_new} حذف شد. ")
                    return
            print("نام کالا پیدا نشد.")
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
    name_csv = input("نام کالا: ").strip()
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
            return
    if not bool_3:
        print(json_pc_2,"\n")
    else:
        print(f" لیست خریداری شده: {json_pc_2}", "\n")
def store_option_11():
    store_option_2()
    if not load_products():
        print("سبد خرید خالی است.")
        return
    print("برای خروج 0 وارد کنید.")
    name = input("نام کالا: ").strip()
    if name == "0":
        return
    ok_2,name_new = check_name(name)
    if not ok_2:
        print(name_new,"\n")
        return
    data = load_products()
    for row,json_data in data.items():
        if name_new == json_data["name"]:
            d = Data(json_data.get("address"))
            ok, masse = d.review()
            if not ok:
                print(masse,"\n")
                return
            bool_1, masse_2 = d.photo(f"new_{row}.{masse}",name_new,json_data["price"],json_data["stock"])
            if not bool_1:
                print(masse_2,"\n")
                return
            page = Path("card.html")
            page.write_text(masse_2,encoding="utf-8")
            webbrowser.open(page.resolve().as_uri())
            return
    print("نام پیدا نشد.","\n")
    return

def store_option_12():
    print("برای خروج 0 وارد کنید.")
    data = input("آدرس سایت را وارد کنید: ").strip()
    if data == "0":
        return
    ok, mass = address_new(data)
    if not ok:
        print(mass,"\n")
        return
    allowed = {"text/html":"html","application/json":"json","text/plain":"text","image/jpeg": "jpg", "image/png": "png"}
    try:
        r = requests.get(url=data, timeout=15)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "").split(";")[0]
        pas = allowed.get(content_type)
        if pas == "html" or pas == "text":
            Path("pay.html").write_text(r.text,encoding="utf-8")
            webbrowser.open(Path("pay.html").resolve().as_uri())
            return
        if pas == "jpg" or pas == "png":
           Path(f"num.{pas}").write_bytes(r.content)
           webbrowser.open(Path(f"unm.{pas}").resolve().as_uri())
           return
        if pas == "json":
            with open("data_new.json","w",encoding="utf-8") as f:
                json.dump(r.json(),f,ensure_ascii=False,indent=4)
                webbrowser.open(Path("data_new.json").resolve().as_uri())
                return
    except requests.exceptions.HTTPError as e:
        print(f"خطای:{e.response.status_code}","\n")
        return
    except requests.exceptions.Timeout:
        print("زمان تمام شد.","\n")
        return
    except requests.exceptions.ConnectionError:
        print("اتصال با سرور برقرار نشد.","\n")
        return
    except requests.exceptions.RequestException:
        print("ارتباط ربات به سایت با مشکل روبه رو شد","\n")
        return