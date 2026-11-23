# storage.py----------------------
import json, csv, os

def load_products(name_file = "products.json"):
    try:
        with open(name_file,"r",encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}

def save_products(products,filename= "products.json"):
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(products,f,ensure_ascii=False,indent=2)

def save_store_csv(data, filename="store.csv"):
    file_is_new = not os.path.exists(filename) or os.path.getsize(filename) == 0
    with open(filename, "a", newline="", encoding="utf-8-sig") as file:
        wri = csv.DictWriter(file, fieldnames=["name","price","id","number","address"])
        if file_is_new:
            wri.writeheader()
        if isinstance(data,list):
            wri.writerows(data)
        else:
            wri.writerow(data)