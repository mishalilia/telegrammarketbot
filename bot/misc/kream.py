from env_var import email, password
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


credentials = {
    "email": email,
    "password": password
}


class Selenium:
    driver = None
    count = 0


def initialize_selenium():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                         " (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')

    Selenium.driver = webdriver.Chrome(options=options)
    login()


def login():
    Selenium.driver.get("https://kream.co.kr/login/")

    # inputs
    WebDriverWait(Selenium.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(credentials.get("email"))

    WebDriverWait(Selenium.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(credentials.get("password"))

    # login click
    WebDriverWait(Selenium.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='login_btn_box']"))).click()

    # waiting for url change
    WebDriverWait(Selenium.driver, 10).until(EC.url_changes("https://kream.co.kr/login/"))
    print("Selenium has been initialized.")


async def product_check(size, link):
    try:
        # going to product page
        Selenium.driver.get(link)

        # clicking buy button
        WebDriverWait(Selenium.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn_division buy']"))).click()

        # getting all costs and sizes
        buttons = WebDriverWait(Selenium.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='link_inner']")))

        # getting available sizes
        for button in buttons:
            oversize = []
            text = button.text.split("\n")
            if "-" in text[0]:
                oversize = ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]
                oversize = oversize[oversize.index(text[0].split("-")[0]):oversize.index(text[0].split("-")[1]) + 1]
            if (text[0] == size or size in oversize) and text[1] != "구매입찰":
                return text[1].replace(",", "")

        return False

    # in case site of product couldn't load properly
    except TimeoutException:
        return await product_check(size, link)
