# reports.py---------
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from storage import load_products
import csv
def export_excel(filename_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "خریدها"
    ws.sheet_view.rightToLeft = True
    ws.append(["نام","قیمت","ایدی","تعداد","ادرس","جمع"])
    num = 0
    with open("store.csv", mode="r", newline="", encoding="utf-8-sig") as file:
        data = csv.DictReader(file)
        for wer in data:
            name = wer["name"]
            price = int(wer["price"])
            new_id = int(wer["id"])
            number = int(wer["number"])
            num += number
            address = wer.get("address","")
            ws.append([name, price, new_id, number, address, price * number])
    last = ws.max_row
    ws.cell(row=last+1,column=3,value="فروش شما:")
    total = 0
    for (value,) in ws.iter_rows(min_row=2,min_col=2,max_col=2,values_only=True):
        if isinstance(value, (int, float)):
            total += value * num
    ws.cell(row=last+1,column=2,value=total)
    ws.cell(row=last+2,column=3,value="تعداد همه کالا فروخته شده:")
    new_row = 0
    for (new,) in ws.iter_rows(min_row=2,min_col=4,max_col=4,values_only=True):
        if isinstance(new, (int, float)):
            new_row += new
    ws.cell(row=last+2,column=2,value=new_row)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
    for cel in ("B","F"):
        for cell in ws[cel][1:]:
            cell.number_format = "#,##0"
    ws.column_dimensions["A"].width = 20
    ws.freeze_panes = "A2"
    try:
        wb.save(filename_path)
        return True, ""
    except PermissionError:
        return False, "فایل در اکسل باز است."

def export_json(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "سبد_فروش"
    ws.sheet_view.rightToLeft = True
    ws.append(["نام","قیمت","ایدی","تعداد","ادرس","جمع"])
    sum_new = 0
    data_new = load_products()
    if not data_new:
        return False, "انبار خالی است."
    for row, dic in data_new.items():
        name = dic["name"]
        price = int(dic["price"])
        new_id = int(row)
        stock = int(dic["stock"])
        address = dic["address"]
        ws.append([name,price,new_id,stock,address,price*stock])
        sum_new += price * stock
    ws.append(["تعداد کالا باقی مانده", "قیمت فروش کالا", "قیمت تمام کالا انبار"])
    last = ws.max_row
    tot_le = 0
    for (D,) in ws.iter_rows(min_row=2,min_col=4,max_col=4,values_only=True):
        if isinstance(D,(int, float)):
            tot_le += D
    ws.cell(row=last+1, column=1,value=tot_le)
    tot_le = 0
    for (B,) in ws.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        if isinstance(B, (int, float)):
            tot_le += B
    ws.cell(row=last+1,column=2,value=tot_le)
    ws.cell(row=last+1,column=3,value=sum_new)
    ws.append(["تعداد خریدها", "فروش_کامل","پر فروش ترین"])
    try:
        last_new = ws.max_row
        profit = 0
        ted = 0
        dic = {}
        with open("store.csv", "r", newline="", encoding="utf-8-sig") as file:
            data = csv.DictReader(file)
            if not data:
                return False, "سبد_خرید خالی است."
            for ref in data:
                name = ref["name"]
                price_new = int(ref["price"])
                number_new = int(ref["number"])
                dic[ref["name"]] = number_new
                ted += number_new
                profit += price_new * number_new
                dic[name] = dic.get(name, 0) + number_new
            ws.cell(row=last_new + 1,column=1, value=ted)
            ws.cell(row=last_new + 1, column=2, value=profit)
            new = max(dic, key=dic.get)
            ws.cell(row=last_new+1,column=3,value=f"{new}_({dic[new]})")
            ws.freeze_panes = "A2"
            try:
                wb.save(path)
                return True, ""
            except PermissionError:
                return False, "فایل در اکسل باز است."
    except FileNotFoundError:
        return False, "سبد_خرید خالی است."