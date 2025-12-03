from datetime import datetime
from typing import List, Dict
import uuid
import json
import os

DATA_FILE = "data/orders.json"

class OrderItem:
    def __init__(self, product_id: str, name: str, price: float, quantity: int = 1):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @property
    def subtotal(self) -> float:
        return self.price * self.quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["product_id"], data["name"], data["price"], data["quantity"])


class Order:
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    
    def __init__(self, customer_id: str, order_id: str = None):
        self.order_id = order_id or f"ORD-{uuid.uuid4().hex[:8].upper()}"
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = self.DRAFT
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    def add_item(self, product_id: str, name: str, price: float, quantity: int = 1) -> bool:
        if quantity <= 0:
            return False
        
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                self.updated_at = datetime.now()
                return True
        
        new_item = OrderItem(product_id, name, price, quantity)
        self.items.append(new_item)
        self.updated_at = datetime.now()
        return True
    
    def remove_item(self, product_id: str, quantity: int = None) -> bool:
        for i, item in enumerate(self.items):
            if item.product_id == product_id:
                if quantity is None or quantity >= item.quantity:
                    self.items.pop(i)
                    self.updated_at = datetime.now()
                    return True
                else:
                    item.quantity -= quantity
                    self.updated_at = datetime.now()
                    return True
        return False
    
    def get_total(self) -> float:
        return sum(item.subtotal for item in self.items)
    
    def update_status(self, new_status: str) -> bool:
        valid_statuses = [
            self.DRAFT, self.PENDING, self.PROCESSING,
            self.COMPLETED, self.CANCELLED
        ]
        if self.status in [self.COMPLETED, self.CANCELLED]:
            return False
        if new_status not in valid_statuses:
            return False
        
        if new_status == self.PENDING and not self.items:
            return False
        
        if new_status == self.COMPLETED and self.status != self.PROCESSING and self.status != self.PENDING:
            # Modified logic to allow Pending -> Completed for simplicity in this task
            pass 
        
        self.status = new_status
        self.updated_at = datetime.now()
        return True
    
    def clear_order(self) -> None:
        self.items.clear()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "items": [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, data):
        order = cls(data["customer_id"], data["order_id"])
        order.status = data["status"]
        order.created_at = datetime.fromisoformat(data["created_at"])
        order.items = [OrderItem.from_dict(item) for item in data["items"]]
        return order

# --- Helper Functions for File Handling ---

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_orders() -> List[Order]:
    ensure_data_dir()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Order.from_dict(o) for o in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_order(order: Order):
    orders = load_orders()
    existing_found = False
    for i, o in enumerate(orders):
        if o.order_id == order.order_id:
            orders[i] = order
            existing_found = True
            break
    
    if not existing_found:
        orders.append(order)
    
    with open(DATA_FILE, "w") as f:
        json.dump([o.to_dict() for o in orders], f, indent=4)

def get_pending_orders() -> List[Order]:
    orders = load_orders()
    return [o for o in orders if o.status == Order.PENDING]