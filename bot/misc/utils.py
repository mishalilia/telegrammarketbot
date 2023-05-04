import requests
from .kream import product_check
from math import ceil
from bs4 import BeautifulSoup


weights = {
     "S": 1.5,
     "B": 1.5,
     "C": 2,
     "A": 0.3,
     "U": 0.1,
     "T": 0.3,
     "L": 0.4,
     "J": 1,
     "P": 0.5,
     "H": 0.8,
     "D": 0.5,
     "O": 1,
     "V": 0.7,
     "W": 0.5,
}


def is_admin(user_id):
    if user_id in [482256219, 1711454390]:
        return True
    else:
        return False


def coupang(size, link):
    headers = {'referer': 'https://google.com'}
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    available_sizes = [str(int(s.text)) for s in soup.findAll("li", class_="Dropdown-Select__Dropdown__Item")]
    price = soup.find("span", class_="total-price").text.split("원")[0][1:].replace(",", "")
    if size in available_sizes:
        return price
    else:
        return False


def get_delivery_cost(weight):
    weight = ceil(weight / 0.5) * 0.5
    response = requests.get("https://www.google.com/finance/quote/USD-RUB")
    soup = BeautifulSoup(response.text, "html.parser")
    currency = soup.find("div", class_="YMlKec fxKbKc").text
    return int(float(currency) * 21 * weight)


def get_product_cost(cost_krw):
    response = requests.get("https://www.google.com/finance/quote/KRW-RUB")
    soup = BeautifulSoup(response.text, "html.parser")
    currency = soup.find("div", class_="YMlKec fxKbKc").text
    return ceil(float(currency) * cost_krw)


def form_order(products):
    products_str = str()
    products_price = float()
    weight = float()

    for product in products:
        products_str += f"Айди товара: {product['id']}\n" \
                        f"Размер: {product['size']}\n" \
                        f"Цена: {product['price']}₽\n\n"
        products_price += product["price"]
        weight += weights[product["id"][1]]

    delivery_cost = get_delivery_cost(weight)
    products_price = products_price

    return f"{products_str}"\
           f"Стоимость доставки: {delivery_cost}₽\n\n"\
           f"Общая сумма: {products_price + delivery_cost}₽"


def get_price(size, link):
    if "kream.co.kr" in link:
        return product_check(size, link)
    elif "coupang.com" in link:
        return coupang(size, link)
