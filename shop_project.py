# shop_project.py---------------
from storage import load_products
from handlers import (store_option_1,store_option_2,store_option_3,
                      store_option_4,store_option_6,store_option_7,store_option_8,store_option_9,
                      store_option_10,store_option_11,store_option_12,store_option_13)
def main():
    while True:
        options_store = input("1:افزودن کالا در انبار 2:نمایش_انبار  3:حذف شناسه_انبار، 4:تغییر موجودی کالا،\n"
                              " 5:خروج 6:خرید 7: لغو خرید 8:حذف تمام کالا_انبار 9: نمایش خرید 10:جستجو 11:جستجو سایت, 12:ذخیره داده شما 13:نمایش" "\n").strip()
        if options_store == "1":
            store_option_1(load_products())
        elif options_store == "2":
            store_option_2()
        elif options_store == "3":
            store_option_3()
        elif options_store == "4":
            store_option_4()
        elif options_store == "5":
            print("روز خوبی داشته باشید.")
            break
        elif options_store == "6":
            store_option_6()
        elif options_store == "7":
            store_option_7()
        elif options_store == "8":
            store_option_8()
        elif options_store == "9":
            store_option_9()
        elif options_store == "10":
            store_option_10()
        elif options_store == "11":
            store_option_11()
        elif options_store == "12":
            store_option_12()
        elif options_store == "13":
            store_option_13()
if __name__ == "__main__":
    main()