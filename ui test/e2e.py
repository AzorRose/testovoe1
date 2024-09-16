import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Константы
URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
FIRST_NAME = "Egor"
LAST_NAME = "Letov"
POSTAL_CODE = "08079"

class BasePage:
    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):
    def login(self, username, password):
        username_field = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Products" in self.driver.page_source

class ProductsPage(BasePage):
    def add_to_cart(self, item_name):
        add_to_cart_button = self.driver.find_element(By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
        add_to_cart_button.click()

    def go_to_cart(self):
        cart_button = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_button.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Your Cart" in self.driver.page_source

class CartPage(BasePage):
    def check_item_in_cart(self, item_name):
        item_in_cart = self.driver.find_element(By.XPATH, f"//div[text()='{item_name}']")
        assert item_in_cart.is_displayed()

    def go_to_checkout(self):
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Checkout: Your Information" in self.driver.page_source

class CheckoutPage(BasePage):
    def enter_information(self, first_name, last_name, postal_code):
        first_name_field = self.driver.find_element(By.ID, "first-name")
        last_name_field = self.driver.find_element(By.ID, "last-name")
        postal_code_field = self.driver.find_element(By.ID, "postal-code")
        continue_button = self.driver.find_element(By.ID, "continue")

        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        postal_code_field.send_keys(postal_code)
        continue_button.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Checkout: Overview" in self.driver.page_source

    def finish_order(self):
        finish_button = self.driver.find_element(By.ID, "finish")
        finish_button.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert "Checkout: Complete!" in self.driver.page_source

@pytest.fixture(scope="function")
def driver():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    yield driver
    driver.quit()

def test_sausedemo_e2e(driver):
    logging.info("Starting test")

    login_page = LoginPage(driver)
    login_page.login(USERNAME, PASSWORD)

    products_page = ProductsPage(driver)
    products_page.add_to_cart("Sauce Labs Backpack")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.check_item_in_cart("Sauce Labs Backpack")
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.enter_information(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    checkout_page.finish_order()

    logging.info("Test completed successfully")
