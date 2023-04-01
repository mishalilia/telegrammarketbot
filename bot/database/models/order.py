class Order:
    def __init__(self, order_id, user_id, products, location, payment):
        self.order_id = order_id
        self.user_id = user_id
        self.products = products
        # products = {
        #   product_id: {size: SIZE, price: PRICE}
        # }
        self.location = location
        self.payment = payment
