import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver():
    driver_path = "C:\\Users\\USER\\chromedriver\\win64-128.0.6613.85\\chromedriver-win64\\chromedriver.exe"
    service = Service(driver_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

excel_path = r'C:\Users\USER\PycharmProjects\ASALProject\login.xlsx'
df = pd.read_excel(excel_path)

def save_result(row, actual_result, status):
    df.at[row, 'Actual Result'] = actual_result
    df.at[row, 'Status'] = status
    df.to_excel(excel_path, index=False)
    print(f"Row {row + 1}: {status} - {actual_result}")

def test_validLogin1(driver):
    email = df.at[0, 'Email']
    password = df.at[0, 'Password']
    expected_result = df.at[0, 'Expected Result']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    try:
        assert driver.find_element(By.CLASS_NAME, 'woocommerce-MyAccount-content').is_displayed(), "Login failed"
        save_result(0, "Login successful", "Pass")
    except NoSuchElementException:
        save_result(0, "Login failed", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_validLogin2(driver):
    email = df.at[1, 'Email']
    password = df.at[1, 'Password']
    expected_result = df.at[1, 'Expected Result']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    try:
        assert driver.find_element(By.CLASS_NAME, 'woocommerce-MyAccount-content').is_displayed(), "Login failed"
        save_result(1, "Login successful", "Pass")
    except NoSuchElementException:
        save_result(1, "Login failed", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_wrongPassword(driver):
    email = df.at[2, 'Email']
    password = df.at[2, 'Password']
    expected_result = df.at[2, 'Expected Result']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    try:
        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert "incorrect. Lost your password?" in error_message, "Error message not displayed for wrong password"
        save_result(2, error_message, "Pass")
    except NoSuchElementException:
        save_result(2, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_emptyPassword(driver):
    email = df.at[3, 'Email']
    password = ""
    expected_result = df.at[3, 'Expected Result']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    try:
        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert "The password field is empty" in error_message, "Error message not displayed for empty password"
        save_result(3, error_message, "Pass")
    except NoSuchElementException:
        save_result(3, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')


def test_emptyEmail(driver):
    email = ""
    password = df.at[4, 'Password']
    expected_result = df.at[4, 'Expected Result']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    try:
        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert "Username is required" in error_message, "Error message not displayed for empty email"
        save_result(4, error_message, "Pass")
    except NoSuchElementException:
        save_result(4, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')


def test_emptyEmailAndPassword(driver):
    email = ""
    password = ""
    expected_result = df.at[5, 'Expected Result']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    try:

        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert "Username is required" in error_message, "Error message not displayed for empty email and password"
        save_result(5, error_message, "Pass")
    except NoSuchElementException:
        save_result(5, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')










