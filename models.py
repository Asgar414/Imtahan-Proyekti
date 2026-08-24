import json
from typing import List, Optional, Dict, Union

class Product:
    def __init__(self, name: str, quantity: int, price: float):
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self) -> Dict[str, Union[str, int, float]]:
        return {"name": self.name, "quantity": self.quantity, "price": self.price}

class GroceryManager:
    def __init__(self):
        self.items_list: List[Product] = []

    def add_item(self, product: Product) -> str:
        for item in self.items_list:
            if item.name.lower() == product.name.lower():
                item.quantity += product.quantity 
                return "updated"
        self.items_list.append(product)
        return "added"

    def delete_item(self, name: str) -> bool:
        for item in self.items_list:
            if item.name.lower() == name.lower():
                self.items_list.remove(item)
                return True
        return False

    def update_item(self, name: str, new_qty: int, new_price: float) -> bool:
        for item in self.items_list:
            if item.name.lower() == name.lower():
                item.quantity = new_qty
                item.price = new_price
                return True
        return False

    def search_item(self, name: str) -> Optional[Product]:
        for item in self.items_list:
            if item.name.lower() == name.lower():
                return item
        return None

    def get_all_items(self) -> List[Product]:
        return self.items_list

    def save_to_file(self, filename: str = "grocery_data.json"):
        with open(filename, "w", encoding="utf-8") as file:
            data = [item.to_dict() for item in self.items_list]
            json.dump(data, file, indent=4)

    def load_from_file(self, filename: str = "grocery_data.json"):
        self.items_list.clear()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                for row in data:
                    self.items_list.append(Product(row["name"], row["quantity"], row["price"]))
        except FileNotFoundError:
            pass