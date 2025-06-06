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
    wait=WebDriverWait(ch_driver, 50)

    yield ch_driver
    ch_driver.quit()

def login(driver):
    wait = WebDriverWait(driver, 30)

    menu = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "top-menu-profile"))
    )

    ActionChains(driver).move_to_element(menu).perform()


    dropdown_link =wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//ul[contains(@class, "my_profile_dropdown")]//a[text()="Prijavi se"]'))
    )


    dropdown_link.click()

    wait.until(EC.visibility_of_element_located((By.ID,"username_header")))

    driver.find_element(By.ID,"username_header").send_keys("bojanstupar1989@gmail.com")
    driver.find_element(By.ID,"next-step").click()
    wait.until(EC.visibility_of_element_located((By.ID, "password_header")))
    driver.find_element(By.ID,"password_header").send_keys("Celarevo44!")
    driver.find_element(By.NAME,"login").click()

def test_open_chrome_and_go_to_polovni_automobili(driver):

   assert "Automobili " in driver.find_element(By.TAG_NAME,"h1").text,"Not good"


def test_register_successful_on_polovni_automobili(driver):
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID,"email")))

    driver.find_element(By.ID,"email").send_keys("bojanstupar1989+test15@gmail.com")
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


def test_login_succesfully(driver):
   wait = WebDriverWait(driver, 30)
   login(driver)

   email_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"MOJ PROFIL")]'))
    )

   email_text= email_element.text.strip()
   assert "MOJ PROFIL" in email_text,"Error"


def test_login_email_invalid(driver):
   wait = WebDriverWait(driver, 30)
   menu = wait.until(
       EC.presence_of_element_located((By.CLASS_NAME, "top-menu-profile"))
   )

   ActionChains(driver).move_to_element(menu).perform()

   dropdown_link = wait.until(
       EC.visibility_of_element_located(
           (By.XPATH, '//ul[contains(@class, "my_profile_dropdown")]//a[text()="Prijavi se"]'))
   )

   dropdown_link.click()

   wait.until(EC.visibility_of_element_located((By.ID, "username_header")))

   driver.find_element(By.ID, "username_header").send_keys("")
   driver.find_element(By.ID, "next-step").click()

   error_element = wait.until(
       EC.visibility_of_element_located((By.CLASS_NAME, "log_error"))
   )

   # Extract and assert the text
   error_text = error_element.text.strip()
   assert "Ne postoji nalog sa ovom mail adresom." in error_text,"Error"


def test_login_password_invalid(driver):
    wait = WebDriverWait(driver, 30)
    menu = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "top-menu-profile"))
    )

    ActionChains(driver).move_to_element(menu).perform()

    dropdown_link = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//ul[contains(@class, "my_profile_dropdown")]//a[text()="Prijavi se"]'))
    )

    dropdown_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "username_header")))

    driver.find_element(By.ID, "username_header").send_keys("bojanstupar1989@gmail.com")
    driver.find_element(By.ID, "next-step").click()

    driver.find_element(By.ID,"password_header").send_keys("Cela")
    driver.find_element(By.NAME, "login").click()

    alert_element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "uk-alert-danger"))
    )


    alert_text = alert_element.text.strip()
    assert "Proveri da li si dobro uneo e-mail i/ili šifru" in alert_text,"Error"

def test_login_click_forgot_password_link(driver):
    wait = WebDriverWait(driver, 50)
    menu = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "top-menu-profile"))
    )

    ActionChains(driver).move_to_element(menu).perform()

    dropdown_link = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//ul[contains(@class, "my_profile_dropdown")]//a[text()="Prijavi se"]'))
    )

    dropdown_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "username_header")))

    driver.find_element(By.ID, "username_header").send_keys("bojanstupar1989@gmail.com")
    driver.find_element(By.ID, "next-step").click()

    driver.find_element(By.ID, "password_header").send_keys("")

    driver.find_element(By.ID,"forgot_password").click()

    send_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Pošalji']"))
    )

    # Click the button
    send_button.click()










