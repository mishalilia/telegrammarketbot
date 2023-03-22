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


def get_sizes(size, link):
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                         " (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # initializing driver
    driver = webdriver.Chrome(options=options)

    try:
        # going to login page
        driver.get("https://kream.co.kr/login/")

        # getting elements
        email = driver.find_element(By.XPATH, "//input[@type='email']")
        password = driver.find_element(By.XPATH, "//input[@type='password']")
        login = driver.find_element(By.XPATH, "//div[@class='login_btn_box']")

        # doing inputs
        email.send_keys(credentials.get("email"))
        password.send_keys(credentials.get("password"))

        # clicking login button
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(login))
        login.click()

        # waiting for url change
        WebDriverWait(driver, 5).until(EC.url_changes("https://kream.co.kr/login/"))

        # going to product page
        driver.get(f"https://kream.co.kr/products/{link}")

        # clicking buy button
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn_division buy']"))).click()

        # getting all costs and sizes
        buttons = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='link_inner']")))

        # getting available sizes
        available_sizes = []
        for button in buttons:
            text = button.text.split("\n")
            if text[1] != "구매입찰":
                available_sizes.append(text[0])

        # returning result
        if size in available_sizes:
            return True
        else:
            return False

    # in case site of product couldn't load properly or login went unsuccessfully
    except TimeoutException:
        return get_sizes(size, link)

    # closing and quiting driver
    finally:
        driver.close()
        driver.quit()


#get_sizes("230", "107181")
