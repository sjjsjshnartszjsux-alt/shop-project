# api.py---------------
import requests, csv, json, os
class Internet:
    def __init__(self,address,userid,id_user,title, body):
        self.address = address
        self.id_user = id_user
        self.userId = userid
        self.title = title
        self.body = body

    def check_user(self,new_user):
        if not new_user:
            return False, "عدد کاربر وارد نشد."
        if not new_user.isdigit():
            return False, "شماره کاربر فقط باید به عدد وارد شود."
        self.userId = new_user
        return True, ""

    def check_id(self,new_id):
        if not new_id:
            return False, "ایدی کاربر وارد نشد."
        if not new_id.isdigit():
            return False, "ایدی فقط باید عدد باشد"
        self.id_user = new_id
        return True, ""

    def chock_title(self,new_title):
        if not new_title:
            return False, "متن اول وارد نشد."
        if new_title.startswith("0"):
            return False, "متن اول نباید با 0 شروع شود."
        self.title = new_title
        return True, "متن اول ذخیره شد."

    def chock_body(self,body):
        if not body:
            return False, "متن دوم وارد نشد."
        if body.startswith("0"):
            return False, "متن دوم نباید با 0 شروع شود."
        self.body = body
        return True, "متن دوم ذخیره شد."

    def search_internet(self):
        file_is_new = not os.path.exists("data_new.json") or os.path.getsize("data_new.json") == 0
        try:
            rou = requests.get(url=f"{self.address}", timeout=10)
            rou.raise_for_status()
            if file_is_new:
                with open("data_new.json","a",newline="",encoding="utf-8-sig") as f:
                    json.dump(rou.json(),f,ensure_ascii=False,indent=4)
            r = requests.get(url=f"{self.address}/{self.id_user}",params={"userId":self.userId}, timeout=10)
            r.raise_for_status()
            if not int(self.userId) == r.json()["userId"]:
                return False, "شناسه یا نام معتبر نیست."
            return True, r.json()
        except requests.exceptions.HTTPError as e:
            return False, f" کد خطا:{e.response}"
        except requests.exceptions.Timeout:
            return False, "زمان تمام شد."
        except requests.exceptions.ConnectionError:
            return False, "اتصال برقرار نشد. :( "

    def create_post(self,title, body,user):
        file = "data.csv"
        try:
            r = requests.post(url=f"{self.address}",json={"title":title,"body":body,"userId":user}, timeout=15)
            r.raise_for_status()
            data = r.json()
            address = r.url
            file_is_new = not os.path.exists(file) or os.path.getsize(file) == 0
            with open(file, "a", newline="", encoding="utf-8-sig") as file:
                wri = csv.DictWriter(file, fieldnames=["title","body","userId",'id',"address"])
                if file_is_new:
                    wri.writeheader()
                data["address"] = address
                wri.writerow(data)
                return data, r.status_code
        except requests.exceptions.HTTPError as e:
            return False, f" خطا: {e.response.status_code}"
        except requests.exceptions.Timeout:
            return False, "زمان تمام شد."
        except requests.exceptions.ConnectionError:
            return False, f" اتصال برقرار نشد. "

    def to_data(self):
        data_json = []
        lis_csv = []
        try:
            with open("data_new.json", "r",encoding="utf-8-sig") as file:
                data = list(json.load(file))
                data_json.append(data)
            with open("data.csv","r",newline="",encoding="utf-8-sig") as f:
                new_data = list(csv.DictReader(f))
                lis_csv.append(new_data)
                return new_data, self.address, data
        except FileNotFoundError:
            return lis_csv, "[]", data_json

class Ticket:
    def __init__(self,price):
        self.price = price
    def can_buy(self,money_user,quantity):
        total = int(self.price) * int(quantity)
        return int(money_user) >= total