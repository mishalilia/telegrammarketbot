import sqlite3


class Db:
    def __init__(self):
        # connecting to db
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

        # creating tables
        try:
            self.cur.execute("CREATE TABLE products("
                             "product_id TEXT NOT NULL UNIQUE,"
                             "link TEXT NOT NULL UNIQUE)")
            self.cur.execute("CREATE TABLE orders("
                             "order_id TEXT NOT NULL UNIQUE,"
                             "user_id TEXT NOT NULL,"
                             "product_id TEXT NOT NULL,"
                             "size TEXT NOT NULL,"
                             "location TEXT NOT NULL)")
            self.con.commit()

        except sqlite3.OperationalError:
            pass
