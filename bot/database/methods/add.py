from sqlite3 import IntegrityError


def add_product(db, product_id, link):
    try:
        db.cur.execute("INSERT INTO products VALUES(?, ?)", (product_id, link,))
        db.con.commit()
        return "✅ Товар добавлен."
    except IntegrityError:
        return "❌ Товар с таким айди или ссылкой уже имеется."


def add_order(db, order_id, user_id, product_id, size, location):
    try:
        db.cur.execute("INSERT INTO orders VALUES(?, ?, ?, ?, ?)", (order_id, user_id, product_id, size, location,))
        db.con.commit()
        return True
    except IntegrityError:
        return False
