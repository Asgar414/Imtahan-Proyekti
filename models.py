import json

class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    # Obyekti JSON formatında yadda saxlamaq üçün dictionary-ə çeviririk
    def to_dict(self):
        return {"name": self.name, "quantity": self.quantity, "price": self.price}

class GroceryManager:
    def __init__(self):
        self.items_list = []

    def add_item(self, product):
        # Eyni adlı məhsul varsa, sadəcə sayını artırırıq (Tapşırıqdakı "Unikallıq" tələbi)
        for item in self.items_list:
            if item.name.lower() == product.name.lower():
                item.quantity += product.quantity 
                return "Updated"
        
        # Yoxdursa, yeni məhsulu siyahıya əlavə edirik
        self.items_list.append(product)
        return "Added"

    def delete_item(self, name):
        for item in self.items_list:
            if item.name.lower() == name.lower():
                self.items_list.remove(item)
                return True
        return False

    def update_item(self, name, new_qty, new_price):
        for item in self.items_list:
            if item.name.lower() == name.lower():
                item.quantity = new_qty
                item.price = new_price
                return True
        return False

    def search_item(self, name):
        for item in self.items_list:
            if item.name.lower() == name.lower():
                return item
        return None

    def get_all_items(self):
        return self.items_list

    def save_to_file(self, filename="grocery_data.json"):
        with open(filename, "w") as file:
            # Siyahıdakı hər bir Product obyektini dict-ə çevirib fayla yazırıq
            data = [item.to_dict() for item in self.items_list]
            json.dump(data, file, indent=4)

    def load_from_file(self, filename="grocery_data.json"):
        self.items_list.clear() # Yükləməzdən əvvəl köhnə siyahını təmizləyirik
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for row in data:
                    new_product = Product(row["name"], row["quantity"], row["price"])
                    self.items_list.append(new_product)
        except FileNotFoundError:
            pass # Fayl yoxdursa, heç nə etmə