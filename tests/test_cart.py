import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

@pytest.fixture
def setup_driver():
    service = Service("C:/Users/USER/chromedriver/win64-128.0.6613.85/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def add_products_to_cart(driver, num_items=4):
    try:

        driver.get("http://demostore.supersqa.com/")
        buttons = driver.find_elements(By.CSS_SELECTOR, "a.add_to_cart_button")

        if not buttons:
            print("No 'Add to Cart' buttons found")
            return

        items_to_add = min(num_items, len(buttons))
        if items_to_add == 0:
            print("No items available to add to the cart")
            return

        for index in range(items_to_add):
            buttons[index].click()
            time.sleep(2)

    except TimeoutException:
        print("Page load timed out.")

def check_cart_items(driver):
    try:
        driver.get("http://demostore.supersqa.com/cart/")
        items_in_cart = driver.find_elements(By.CLASS_NAME, "cart_item")

        if not items_in_cart:
            print("No items found in the cart")
            return []

        print("Items added successfully:", len(items_in_cart) == 4)
        print(f"Items in the cart: {len(items_in_cart)}")

        subtotal = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount").text
        print(f"Cart subtotal: {subtotal}")

        return items_in_cart

    except NoSuchElementException:
        print("Could not find cart item elements or subtotal.")
    except Exception as e:
        print(f"An error occurred while checking cart items: {e}")
    return []


def remove_one_item(driver):
    try:
        remove_btn = driver.find_element(By.CLASS_NAME, "remove")
        remove_btn.click()
        time.sleep(3)

        updated_subtotal = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount").text
        print(f"Subtotal after item removal: {updated_subtotal}")

    except NoSuchElementException:
        print("Remove button or subtotal not found")
    except Exception as e:
        print(f"An error occurred while removing an item: {e}")


def test_cart_operations(setup_driver):
    add_products_to_cart(setup_driver, 4)
    cart_items = check_cart_items(setup_driver)

    if cart_items:
        remove_one_item(setup_driver)







