import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


@pytest.fixture()
def driver():
    ch_driver = webdriver.Chrome(service=Service('C:/Windows/chromedriver.exe'))
    ch_driver.maximize_window()
    ch_driver.get('https://polovniautomobili.com/')
    wait=WebDriverWait(ch_driver, 30)

    yield ch_driver
    ch_driver.quit()

def test_open_chrome_and_go_to_polovni_automobili(driver):

   assert "Automobili " in driver.find_element(By.TAG_NAME,"h1").text,"Not good"


def test_register_successful_on_polovni_automobili(driver):
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID,"email")))

    driver.find_element(By.ID,"email").send_keys("bojanstupar1989+test5@gmail.com")
    driver.find_element(By.ID,"password_first").send_keys("Celarevo44!")
    driver.find_element(By.ID,"password_second").send_keys("Celarevo44!")

    driver.find_element(By.ID, "tos").click()
    driver.find_element(By.ID,"easySaleConsent").click()
    driver.find_element(By.ID,"easyBuyConsent").click()

    driver.find_element(By.NAME, "login").click()

    register_text=wait.until(EC.presence_of_element_located((By.TAG_NAME,"p"))).text.strip()
    assert "Hvala na registraciji!" in register_text,"Error"


def test_register_email_and_password_required_fields_validation(driver):

    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("")
    driver.find_element(By.ID, "password_first").send_keys("")
    driver.find_element(By.ID, "password_second").send_keys("")

    driver.find_element(By.NAME, "login").click()

    active_element = driver.switch_to.active_element


    message = active_element.get_attribute("validationMessage")

    assert "Please fill out this field" in message, "Error"

def test_register_password_invalid_format(driver):
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test7@gmail.com")
    driver.find_element(By.ID, "password_first").send_keys("Cela")
    driver.find_element(By.ID, "password_second").send_keys("Cela")

    driver.find_element(By.ID, "tos").click()
    driver.find_element(By.ID, "easySaleConsent").click()
    driver.find_element(By.ID, "easyBuyConsent").click()

    driver.find_element(By.NAME, "login").click()

    error = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class,'uk-alert-danger')]//p[contains(text(),'Šifra je kraća')]")
    ))

    assert "Šifra je kraća od 8 znakova" in error.text, "Error"

def test_register_password_missmatch_error(driver):
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test9@gmail.com")
    driver.find_element(By.ID, "password_first").send_keys("Celarevo44!")
    driver.find_element(By.ID, "password_second").send_keys("Cela")

    driver.find_element(By.ID, "tos").click()
    driver.find_element(By.ID, "easySaleConsent").click()
    driver.find_element(By.ID, "easyBuyConsent").click()

    driver.find_element(By.NAME, "login").click()

    error = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class,'uk-alert-danger')]//p[contains(text(),'Šifra i ponovljena šifra')]")
    ))

    assert "Šifra i ponovljena šifra se ne podudaraju" in error.text, "Error"

def test_register_email_already_exists(driver):
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989@gmail.com")
    driver.find_element(By.ID, "password_first").send_keys("Celarevo44!")
    driver.find_element(By.ID, "password_second").send_keys("Celarevo44!")

    driver.find_element(By.ID, "tos").click()
    driver.find_element(By.ID, "easySaleConsent").click()
    driver.find_element(By.ID, "easyBuyConsent").click()

    driver.find_element(By.NAME, "login").click()

    error_element = wait.until(
        EC.visibility_of_element_located((By.ID, "register_email_error"))
    )


    error_text = error_element.text.strip()

    assert "Uneta E-mail adresa je već zauzeta" in error_text

def test_register_tos_required(driver):
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test90@gmail.com")
    driver.find_element(By.ID, "password_first").send_keys("Celarevo44!")
    driver.find_element(By.ID, "password_second").send_keys("Celarevo44!")

    driver.find_element(By.ID, "easySaleConsent").click()
    driver.find_element(By.ID, "easyBuyConsent").click()

    driver.find_element(By.NAME, "login").click()


    is_invalid = driver.find_element(By.ID, "tos").get_attribute("validationMessage")

    assert "Please check this box if you want to proceed." in is_invalid, "Error"


