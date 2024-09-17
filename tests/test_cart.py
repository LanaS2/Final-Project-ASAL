import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

@pytest.fixture
def setup_driver():
    service = Service("C:/Users/USER/chromedriver/win64-128.0.6613.85/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def add_products_to_cart(driver, num_items=4):
    driver.get("http://demostore.supersqa.com/")

    time.sleep(3)
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.add_to_cart_button")

    items_to_add = min(num_items, len(buttons))
    if items_to_add == 0:
        print("No items available to add to the cart")
        return

    for index in range(items_to_add):
        buttons[index].click()
        time.sleep(2)


def get_cart_subtotal(driver):
    time.sleep(2)
    try:
        subtotal_element = driver.find_element(By.CLASS_NAME, "woocommerce-Price-amount")
        return subtotal_element.text
    except NoSuchElementException:
        print("Subtotal not found")
        return None

def check_cart_items(driver):
    driver.get("http://demostore.supersqa.com/cart/")
    time.sleep(3)
    try:
        items_in_cart = driver.find_elements(By.CLASS_NAME, "cart_item")

        if not items_in_cart:
            print("No items found in the cart")
            return [], None

        subtotal = get_cart_subtotal(driver)
        print(f"Cart subtotal: {subtotal}")
        return items_in_cart, subtotal

    except NoSuchElementException:
        print("Could not find cart item elements or subtotal.")
        return [], None
    except Exception as e:
        print(f"An error occurred while checking cart items: {e}")
        return [], None

def remove_one_item(driver):
    try:
        remove_btn = driver.find_element(By.CLASS_NAME, "remove")
        remove_btn.click()
        time.sleep(3)

        updated_subtotal = get_cart_subtotal(driver)
        print(f"Subtotal after item removal: {updated_subtotal}")
        return updated_subtotal

    except NoSuchElementException:
        print("Remove button or subtotal not found")
        return None
    except Exception as e:
        print(f"An error occurred while removing an item: {e}")
        return None


def test_cart_operations(setup_driver):
    driver = setup_driver
    add_products_to_cart(driver, 4)

    cart_items, original_subtotal = check_cart_items(driver)

    if cart_items:
        updated_subtotal = remove_one_item(driver)

        if original_subtotal and updated_subtotal:
            print(f"Original subtotal: {original_subtotal}")
            print(f"Updated subtotal: {updated_subtotal}")










