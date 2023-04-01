import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from bot.database.models import Order, Product


class FirebaseDB:
    def __init__(self):
        cred = credentials.Certificate(".env")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_product(self, product_id, link):
        product_ref = self.db.collection("products").document(product_id)
        product_ref.set({"link": link})
        return "✅ Товар добавлен."

    def add_order(self, order_id, user_id, products, location, payment):
        order_ref = self.db.collection("orders").document(order_id)
        order_ref.set({
            "user_id": user_id,
            "products": products,
            "location": location,
            "payment": payment
        })
        return True

    def get_product_by_id(self, product_id):
        try:
            product_ref = self.db.collection("products").document(product_id)
            if product_ref.get().to_dict():
                link = product_ref.get().to_dict()["link"]
                product = Product(product_id, link)
                return product
            else:
                return None
        except Exception:
            return None

    def get_product_by_link(self, link):
        product_ref = self.db.collection("products").where("link", "==", link)
        if len(product_ref.get()) > 0:
            product_id = product_ref.get()[0].to_dict()["product_id"]
            product = Product(product_id, link)
            return product
        else:
            return None

    def get_order(self, order_id):
        order_ref = self.db.collection("orders").document(order_id).get().to_dict()
        if order_ref.get().to_dict():
            user_id, products, location, payment = order_ref["user_id"], order_ref["products"],\
                                                   order_ref["location"], order_ref["payment"]
            order = Order(order_id, user_id, products, location, payment)
            return order
        else:
            return None

    def get_all_orders(self):
        orders_ref = self.db.collection("orders")
        orders = [Order(order.id, order.to_dict()["user_id"], order.to_dict()["products"],
                        order.to_dict()["location"], order.to_dict()["payment"])
                  for order in orders_ref.stream()]
        return orders

    def delete_product_by_id(self, product_id):
        product_ref = self.db.collection("products").document(product_id)
        if product_ref.get().to_dict():
            product_ref.delete()
            return "✅ Товар удалён."
        else:
            return "❌ Товар не найден."

    def delete_product_by_link(self, link):
        product_ref = self.db.collection("products").where("link", "==", link)
        if len(product_ref.get()) > 0:
            product_ref.get()[0].reference.delete()
            return "✅ Товар удалён."
        else:
            return "❌ Товар не найден."

    def delete_order(self, order_id):
        order_ref = self.db.collection("orders").document(order_id)
        if order_ref.get().to_dict():
            order_ref.delete()
            return "✅ Заказ удалён."
        else:
            return "❌ Заказ не найден."


db = FirebaseDB()
