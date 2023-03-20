from bot.database.models import Order, Product


def get_product_by_id(db, product_id):
    try:
        db.cur.execute("SELECT link FROM products WHERE product_id = ?", (product_id,))
        link = db.cur.fetchone()[0]
        product = Product(product_id, link)
        return product
    except Exception:
        return None


def get_product_by_link(db, link):
    try:
        link = link.split("/")[-1]
        db.cur.execute("SELECT product_id FROM products WHERE link = ?", (link,))
        product_id = db.cur.fetchone()[0]
        product = Product(product_id, link)
        return product
    except Exception:
        return None


def get_order(db, order_id):
    try:
        db.cur.execute("SELECT user_id, product_id, size, location FROM orders WHERE order_id = ?", (order_id,))
        user_id, product_id, size, location = db.cur.fetchone()
        order = Order(order_id, user_id, product_id, size, location)
        return order
    except Exception:
        return None


def get_all_orders(db):
    db.cur.execute("SELECT * FROM orders")
    orders = [Order(order_id, user_id, product_id, size, location)
              for order_id, user_id, product_id, size, location in db.cur.fetchall()]
    return orders
