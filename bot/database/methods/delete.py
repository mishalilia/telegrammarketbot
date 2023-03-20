from .get import get_product_by_id, get_product_by_link, get_order


def delete_product_by_id(db, product_id):
    if get_product_by_id(db, product_id) is not None:
        db.cur.execute("DELETE FROM products WHERE product_id == ?", (product_id,))
        db.con.commit()
        return "✅ Товар удалён."
    else:
        return "❌ Товар не найден."


def delete_product_by_link(db, link):
    if get_product_by_link(db, link) is not None:
        link = link.split("/")[-1]
        db.cur.execute("DELETE FROM products WHERE link == ?", (link,))
        db.con.commit()
        return "✅ Товар удалён."
    else:
        return "❌ Товар не найден."


def delete_order(db, order_id):
    if get_order(db, order_id):
        db.cur.execute("DELETE FROM orders WHERE order_id == ?", (order_id,))
        db.con.commit()
        return "✅ Заказ удалён."
    else:
        return "❌ Заказ не найден."
