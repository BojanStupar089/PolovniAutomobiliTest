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

def test_polovni_automobili_youtube_link(driver):
    wait = WebDriverWait(driver, 30)
    youtube_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[contains(@href, "youtube.com/user/polovniautomobili")]')
    ))


    youtube_link.click()

def test_polovni_automobili_brza_pretraga_and_click_najnoviji_oglasi(driver):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)


    brza_pretraga = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'BRZA PRETRAGA')]")))
    actions.move_to_element(brza_pretraga).perform()


    najnoviji_oglasi = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Najnoviji oglasi")))
    najnoviji_oglasi.click()

    najnoviji_oglasi=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.searchTitle")))

    assert "Najnoviji oglasi automobila" in najnoviji_oglasi.text,"Error"

def test_polovni_automobili_brza_pretraga_and_click_online_prodavnica(driver):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    brza_pretraga = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'BRZA PRETRAGA')]")))
    actions.move_to_element(brza_pretraga).perform()

    online_prodavnica = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Online prodavnica")))
    online_prodavnica.click()

    online_shop = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h2")))

    assert "Majica" in online_shop.text,"Error"


def test_polovni_automobili_ponuda_vozila_and_click_transportna_vozila(driver):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    ponuda_vozila = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'PONUDA VOZILA')]")))
    actions.move_to_element(ponuda_vozila).perform()

    transportna_vozila=wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transportna vozila")))
    transportna_vozila.click()

    transportna_vozila_title=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.home-title.uk-text-center-small")))

    assert "Kombi i laka dostavna vozila" in transportna_vozila_title.text,"Error"

def test_polovni_automobili_delovi_and_oprema_click_elektrika_and_elektronika(driver):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    delovi_i_oprema = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'DELOVI I OPREMA')]")))
    actions.move_to_element(delovi_i_oprema).perform()

    elektrika_i_elektronika = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Elektrika i elektronika")))
    elektrika_i_elektronika.click()

    elektrika_i_elektronika_title=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"searchTitle")))

    assert "Elektrika i elektronika - auto delovi" in elektrika_i_elektronika_title.text,"Error"


def test_polovni_automobili_delovi_and_oprema_click_delovi_and_oprema_search_motorcycle_case(driver):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    delovi_i_oprema = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'DELOVI I OPREMA')]")))
    actions.move_to_element(delovi_i_oprema).perform()

    delovi_i_oprema_za_motore = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Delovi i oprema za motore")))
    delovi_i_oprema_za_motore.click()

    wait.until(EC.visibility_of_element_located((By.ID,"text_search")))
    driver.find_element(By.ID,"text_search").send_keys("kofer")
    driver.find_element(By.ID,"partsCondition_0").click()
    driver.find_element(By.ID,"submit").click()

    delovi_i_oprema_za_motore_title=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"searchTitle")))

    assert "Pretraga opreme za motore" in delovi_i_oprema_za_motore_title.text,"Error"


def test_polovni_automobili_usluge_and_krediti(driver):
    wait = WebDriverWait(driver, 20)
    actions = ActionChains(driver)

    usluge_i_krediti = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'USLUGE I KREDITI')]")))
    actions.move_to_element(usluge_i_krediti).perform()
    usluge_i_krediti.click()

    ponuda_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.buttonOrder.paOrangeButtonPrimary[href='/paketi-kredita']")
     ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ponuda_btn)
    ponuda_btn.click()

    krediti_text=driver.find_element(By.TAG_NAME,"h1").text

    assert "Krediti - najefikasnije sredstvo plaćanja" in krediti_text,"Error"

def test_polovni_automobili_o_nama(driver):
    wait = WebDriverWait(driver, 10)

    # Skroluj skroz do dna stranice
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # sačekaj da se footer elementi učitaju

    # Sačekaj i pronađi link "O nama"
    o_nama_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "O nama")))

    # Klikni na link
    o_nama_link.click()

    o_nama_text=driver.find_element(By.TAG_NAME,"h1").text
    assert "O sajtu Polovniautomobili.com" in o_nama_text,"Error"


def test_polovni_automobili_click_apex_automobili_bussiness_link(driver):
    wait = WebDriverWait(driver, 40)

    biznis_link = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'a[href="/lista-biznis-prodavaca"]')
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", biznis_link)
    biznis_link.click()

    apex_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a.dealerLogoHolder[href^="/apex-automobili"]')
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apex_link)
    apex_link.click()

    apex_title=driver.find_element(By.TAG_NAME,"h1").text
    assert "APEX automobili" in apex_title,"Error"





