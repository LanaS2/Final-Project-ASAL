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

excel_path = r'C:\Users\USER\PycharmProjects\ASALProject\Registration.xlsx'
df = pd.read_excel(excel_path)

def save_result_registration(row, actual_result, status):
    df.at[row, 'Registration Result'] = actual_result
    df.at[row, 'Registration Status'] = status
    df.to_excel(excel_path, index=False)
    print(f"Row {row + 1}: {status} - {actual_result}")

def test_validRegistrationStrongPassword(driver):
    email = df.at[0, 'Email']
    password = df.at[0, 'Password']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.ID, 'reg_email').send_keys(email)
    driver.find_element(By.ID, 'reg_password').send_keys(password)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    try:
        success_message = driver.find_element(By.CLASS_NAME, 'woocommerce-MyAccount-content').text
        assert "Hello" in success_message, "Registration failed"
        save_result_registration(0, "Registration successful", "Pass")
    except NoSuchElementException:
        save_result_registration(0, "Registration failed", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_validRegistrationMediumPassword(driver):
    email = df.at[1, 'Email']
    password = df.at[1, 'Password']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.ID, 'reg_email').send_keys(email)
    driver.find_element(By.ID, 'reg_password').send_keys(password)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    try:
        success_message = driver.find_element(By.CLASS_NAME, 'woocommerce-MyAccount-content').text
        assert "Hello" in success_message, "Registration failed"
        save_result_registration(1, "Registration successful", "Pass")
    except NoSuchElementException:
        save_result_registration(1, "Registration failed", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_Registeredaccount(driver):
    email = df.at[2, 'Email']
    password = df.at[2, 'Password']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.ID, 'reg_email').send_keys(email)
    driver.find_element(By.ID, 'reg_password').send_keys(password)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    try:
        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert "An account is already registered with your email address" in error_message, "Error message not displayed for already registered account"
        save_result_registration(2, error_message, "Pass")
    except NoSuchElementException:
        save_result_registration(2, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_validEmailEmptyPassword(driver):
    email = df.at[3, 'Email']
    password = ""

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.ID, 'reg_email').send_keys(email)
    driver.find_element(By.ID, 'reg_password').send_keys(password)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    try:
        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert " Please enter an account password." in error_message, "Error message not displayed for empty password"
        save_result_registration(3, error_message, "Pass")
    except NoSuchElementException:
        save_result_registration(3, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')

def test_emptyEmailStrongPassword(driver):
    email = ""
    password = df.at[4, 'Password']

    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.ID, 'reg_email').send_keys(email)
    driver.find_element(By.ID, 'reg_password').send_keys(password)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    try:
        error_message = driver.find_element(By.CLASS_NAME, 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
        assert "Please provide a valid email address." in error_message, "Error message not displayed for empty email"
        save_result_registration(4, error_message, "Pass")
    except NoSuchElementException:
        save_result_registration(4, "No error message found", "Fail")

    driver.get('http://demostore.supersqa.com/my-account/')








