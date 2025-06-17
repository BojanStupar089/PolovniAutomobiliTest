import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


@pytest.fixture()
def driver():
    ch_driver = webdriver.Chrome(service=Service('C:/Windows/chromedriver-win64/chromedriver.exe'))
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

def accept_cookies(driver):

    try:
        cookie_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "js-accept-cookies"))
        )
        cookie_button.click()
    except TimeoutException:

        pass

def test_open_chrome_and_go_to_polovni_automobili(driver):

   assert "Automobili " in driver.find_element(By.TAG_NAME,"h1").text,"Error"

def test_register_successful_on_polovni_automobili(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID,"email")))

    driver.find_element(By.ID,"email").send_keys("bojanstupar1989+test36@gmail.com")
    driver.find_element(By.ID,"password_first").send_keys("Celarevo44!")
    driver.find_element(By.ID,"password_second").send_keys("Celarevo44!")

    driver.find_element(By.ID, "tos").click()
    driver.find_element(By.ID,"easySaleConsent").click()
    driver.find_element(By.ID,"easyBuyConsent").click()

    driver.find_element(By.NAME, "login").click()

    register_text=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"p"))).text.strip()
    assert "Hvala na registraciji!" in register_text,"Error"

def test_register_email_and_password_required_fields_validation(driver):
    accept_cookies(driver)
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
    accept_cookies(driver)
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
    accept_cookies(driver)
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

    accept_cookies(driver)
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

    error_div = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.uk-alert.uk-alert-danger"))
    )


    error_text = error_div.find_element(By.TAG_NAME, "p").text

    assert "Uneta E-mail adresa je već zauzeta" in error_text, "Expected error message not found"

def test_register_tos_required(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    css_selector = "a.top-menu-register[data-label='Registruj se']"
    registruj_se = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    ActionChains(driver).move_to_element(registruj_se).perform()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test90@gmail.com")
    driver.find_element(By.ID, "password_first").send_keys("Celarevo44!")
    driver.find_element(By.ID, "password_second").send_keys("Celarevo44!")
    time.sleep(2)
    driver.find_element(By.ID, "easySaleConsent").click()
    driver.find_element(By.ID, "easyBuyConsent").click()
    time.sleep(2)
    driver.find_element(By.NAME, "login").click()


    is_invalid = driver.find_element(By.ID, "tos").get_attribute("validationMessage")

    assert "Please check this box if you want to proceed." in is_invalid, "Error"

def test_login_succesfully(driver):
   accept_cookies(driver)
   wait = WebDriverWait(driver, 30)
   login(driver)

   email_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"MOJ PROFIL")]'))
    )

   email_text= email_element.text.strip()
   assert "MOJ PROFIL" in email_text,"Error"

def test_login_email_invalid(driver):

   accept_cookies(driver)
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

    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    menu = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "top-menu-profile"))
    )

    ActionChains(driver).move_to_element(menu).perform()

    dropdown_link = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//ul[contains(@class, "my_profile_dropdown")]//a[text()="Prijavi se"]'))
    )

    driver.execute_script("arguments[0].click()",dropdown_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username_header")))

    driver.find_element(By.ID, "username_header").send_keys("bojanstupar1989@gmail.com")
    driver.find_element(By.ID, "next-step").click()
    time.sleep(2)
    driver.find_element(By.ID,"password_header").send_keys("Cela")
    driver.find_element(By.NAME, "login").click()

    alert_element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "uk-alert-danger"))
    )


    alert_text = alert_element.text.strip()
    assert "Proveri da li si dobro uneo e-mail i/ili šifru" in alert_text,"Error"

def test_login_forgot_password_link(driver):

    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    menu = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "top-menu-profile"))
    )

    ActionChains(driver).move_to_element(menu).perform()

    dropdown_link = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//ul[contains(@class, "my_profile_dropdown")]//a[text()="Prijavi se"]'))
    )

    driver.execute_script("arguments[0].click()",dropdown_link)
    time.sleep(2)

    wait.until(EC.visibility_of_element_located((By.ID, "username_header")))

    driver.find_element(By.ID, "username_header").send_keys("bojanstupar1989@gmail.com")
    time.sleep(2)
    driver.find_element(By.ID, "next-step").click()


    time.sleep(2)
    forget_password_link=driver.find_element(By.ID,"forgot_password")
    driver.execute_script("arguments[0].click()",forget_password_link)

    send_button = wait.until(
         EC.element_to_be_clickable((By.XPATH, "//button[text()='Pošalji']"))
     )

    # # Click the button
    send_button.click()

def test_polovni_automobili_click_youtube_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    youtube_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[contains(@href, "youtube.com/user/polovniautomobili")]')
    ))


    youtube_link.click()

def test_polovni_automobili_click_instagram_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    # Wait for the Instagram link to be present and clickable
    insta_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-label='Instagram']"))
    )


    driver.execute_script("arguments[0].click();", insta_link)

def test_polovni_automobili_settings_my_profile(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login(driver)

    moj_profil = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a.js_ga-event.signin_menu_element[data-label='klik na moj profil']")
    ))

    # Napravi akciju hover (mouse over)
    actions = ActionChains(driver)
    actions.move_to_element(moj_profil).perform()

    podesavanja = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/redirect/podesavanja') and contains(text(), 'Podešavanja')]")
    ))
    podesavanja.click()

    wait.until(EC.visibility_of_element_located((By.ID,"first_name")))
    first_name_text=driver.find_element(By.ID,"first_name")
    first_name_text.clear()
    first_name_text.send_keys("Djuro")

    last_name_text=driver.find_element(By.ID,"last_name")
    last_name_text.clear()
    last_name_text.send_keys("Peric")
    time.sleep(2)

    text_address=driver.find_element(By.ID,"address")
    text_address.clear()
    text_address.send_keys("Rumenacka 23")

    city_text=driver.find_element(By.ID,"city")
    city_text.clear()
    city_text.send_keys("Novi Sad")

    zip_code_text=driver.find_element(By.ID,"zip_code")
    zip_code_text.clear()
    zip_code_text.send_keys("21000")
    time.sleep(3)

    dropdown_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_region .CaptionCont")))
    driver.execute_script("arguments[0].click();", dropdown_toggle)
    time.sleep(2)  # Pusti da se prikaže lista

    # 2. Klikni na "Južno-bački"
    juzno_backi_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'sumo_region')]//li[.//label[normalize-space()='Južno-bački']]")))
    driver.execute_script("arguments[0].click();", juzno_backi_option)
    time.sleep(2)  # Pusti da se selektuje

    # 3. Klikni van menija da potvrdiš izbor (npr. na body)
    driver.find_element(By.TAG_NAME, "body").click()

    time.sleep(2)
    cell_phone_text=driver.find_element(By.ID,"cellphone")
    cell_phone_text.clear()
    cell_phone_text.send_keys("065121234")


    time.sleep(2)
    driver.find_element(By.ID,"submit").click()

def test_polovni_automobili_click_button_post_ad(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login(driver)

    postavi_oglas = driver.find_element(By.CSS_SELECTOR, "a.top-menu-submit-classified")
    driver.execute_script("arguments[0].click();", postavi_oglas)

    postavi_oglas=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Formular za postavku oglasa" in postavi_oglas, "Error"

def test_polovni_automobili_quick_search_and_click_latest_ads(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)


    brza_pretraga = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'BRZA PRETRAGA')]")))
    actions.move_to_element(brza_pretraga).perform()


    najnoviji_oglasi = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Najnoviji oglasi")))
    najnoviji_oglasi.click()

    najnoviji_oglasi=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.searchTitle")))

    assert "Najnoviji oglasi automobila" in najnoviji_oglasi.text,"Error"

def test_polovni_automobili_quick_search_and_click_online_shop(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    brza_pretraga = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'BRZA PRETRAGA')]")))
    actions.move_to_element(brza_pretraga).perform()

    online_prodavnica = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Online prodavnica")))
    online_prodavnica.click()

    online_shop = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h2")))

    assert "Majica" in online_shop.text,"Error"

def test_polovni_automobili_vehicle_offer_and_click_vehicle_transport(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    ponuda_vozila = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'PONUDA VOZILA')]")))
    actions.move_to_element(ponuda_vozila).perform()

    transportna_vozila=wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transportna vozila")))
    transportna_vozila.click()

    transportna_vozila_title=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.home-title.uk-text-center-small")))

    assert "Kombi i laka dostavna vozila" in transportna_vozila_title.text,"Error"

def test_polovni_automobili_parts_and_accessories_click_electricity_and_electronics(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    delovi_i_oprema = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'DELOVI I OPREMA')]")))
    actions.move_to_element(delovi_i_oprema).perform()

    elektrika_i_elektronika = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Elektrika i elektronika")))
    elektrika_i_elektronika.click()

    elektrika_i_elektronika_title=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"searchTitle")))

    assert "Elektrika i elektronika - auto delovi" in elektrika_i_elektronika_title.text,"Error"

def test_polovni_automobili_parts_and_accessories_search_motorcycle_case(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
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

def test_polovni_automobili_services_and_credits(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
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

def test_polovni_automobili_click_bussiness_sellers_link(driver):
    accept_cookies(driver)
    driver.execute_script("window.scrollTo(0, 800);")
    wait = WebDriverWait(driver, 50)

    biznis_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/lista-biznis-prodavaca') and contains(text(), 'Biznis prodavci')]")
    ))
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", biznis_link)

    ActionChains(driver).move_to_element(biznis_link).perform()
    driver.execute_script("arguments[0].click();", biznis_link)

    biznis_title=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Biznis prodavci – pravna lica" in biznis_title,"Error"

def test_polovni_automobili_click_discounted_vehicles_from_the_past_seven_days(driver):
    accept_cookies(driver)
    driver.execute_script("window.scrollTo(0, 800);")
    wait = WebDriverWait(driver, 30)

    discounted_vehicles = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/auto-oglasi/snizena-cena') and contains(text(), 'Vozila sa sniženom cenom u prethodnih 7 dana')]")
    ))
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", discounted_vehicles)

    ActionChains(driver).move_to_element(discounted_vehicles).perform()
    driver.execute_script("arguments[0].click();", discounted_vehicles)

    discounted_vehicles_title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Oglasi automobila sa sniženom cenom u poslednjih 7 dana" in discounted_vehicles_title,"Error"

def test_polovni_automobili_click_sold_in_last_twenty_four_hours(driver):

    accept_cookies(driver)
    driver.execute_script("window.scrollTo(0, 2400);")
    wait = WebDriverWait(driver, 50)

    twenty_four_hours = wait.until(EC.visibility_of_element_located(
        (By.XPATH,
         "//a[contains(text(), 'Prodato u poslednja 24h')]")
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", twenty_four_hours)

    ActionChains(driver).move_to_element(twenty_four_hours).perform()
    driver.execute_script("arguments[0].click();", twenty_four_hours)

    wait.until(lambda driver: len(driver.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])  #

    twenty_four_hours_title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Oglasi prodati u poslednja 24h" in twenty_four_hours_title,"Error"

def test_polovni_automobili_click_autotest_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 20)
    auto_testovi_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/video-sadrzaj"]')
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", auto_testovi_link)
    driver.execute_script("arguments[0].click();", auto_testovi_link)

    auto_testovi_title=driver.find_element(By.TAG_NAME,"h1").text

    assert "Auto-testovi najinteresantnijih modela | Polovniautomobili.com" in auto_testovi_title,"Error"

def test_polovni_automobili_click_car_buying_guide(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    vodic_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a.paBlueButtonTertiary[href="/pomoc-pri-kupovini-automobila"]')
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vodic_link)
    driver.execute_script("arguments[0].click();", vodic_link)

    vodic_title=driver.find_element(By.TAG_NAME,"h1").text
    assert "Vodič za kupovinu automobila" in vodic_title,"Error"

def test_polovni_automobili_search_arteon(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    dropdown_trigger = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.SumoSelect[name='brand'], div.SumoSelect"))
    )
    dropdown_trigger.click()
    time.sleep(2)

    search_input = driver.find_element(By.CSS_SELECTOR, ".SumoSelect.open input")
    search_input.send_keys("Volkswagen")
    time.sleep(2)

    volkswagen_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Volkswagen')]")))
    volkswagen_option.click()
    time.sleep(3)

    # II MODEL

    driver.find_element(By.CSS_SELECTOR, ".sumo_model").click()
    time.sleep(2)


    search_input = driver.find_element(By.CSS_SELECTOR, ".sumo_model .search-txt")
    search_input.send_keys("Arteon")
    time.sleep(2)


    driver.find_element(By.XPATH,
                        "//div[contains(@class, 'sumo_model')]//ul[@class='options']//label[contains(text(), 'Arteon')]").click()
    time.sleep(2)


    ok_button = driver.find_element(By.CSS_SELECTOR, ".sumo_model .btnOk")
    driver.execute_script("arguments[0].click();", ok_button)

    #III Cena do
    driver.find_element(By.ID, "price_to").send_keys("30000")
    time.sleep(2)

    # IV YEAR FROM
    year_value_from = "2017"
    year_label_from = f"{year_value_from} god."


    year_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_year_from .SelectBox")))
    year_dropdown.click()
    time.sleep(3)


    option_label_from = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         f"//div[contains(@class,'sumo_year_from')]//ul[@class='options']//label[normalize-space(text())='{year_label_from}']")
    ))


    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label_from)
    option_label_from.click()
    time.sleep(2)


    caption_label_from = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_year_from > p.CaptionCont.SelectBox")))
    wait.until(lambda d: year_value_from in caption_label_from.text)

    # V YEAR TO

    year_value_to = "2024"
    year_label_to = f"{year_value_to} god."

    year_dropdown_to = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_year_to .SelectBox")))
    year_dropdown_to.click()
    time.sleep(3)

    option_label_to = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         f"//div[contains(@class,'sumo_year_to')]//ul[@class='options']//label[normalize-space(text())='{year_label_to}']")
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label_to)
    option_label_to.click()
    time.sleep(2)

    caption_label_to = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_year_to > p.CaptionCont.SelectBox")))
    wait.until(lambda d: year_value_to in caption_label_to.text)
    time.sleep(2)

    # VI KAROSERIJA
    chassis_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_chassis .SelectBox")))
    chassis_dropdown.click()
    time.sleep(3)


    option_name = "Limuzina"

    option_label = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         f"//div[contains(@class,'sumo_chassis')]//ul[@class='options']//label[normalize-space(text())='{option_name}']")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label)
    time.sleep(2)

    checkbox_span = option_label.find_element(By.XPATH, "./preceding-sibling::span")
    driver.execute_script("arguments[0].click();", checkbox_span)
    time.sleep(2)

    caption_label = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_chassis > p.CaptionCont.SelectBox")))
    wait.until(lambda d: option_name in caption_label.text)

    caption_label.click()

    fuel_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_fuel .SelectBox")))
    fuel_dropdown.click()
    time.sleep(2)

    option_name = "Dizel"

    option_label = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         f"//div[contains(@class,'sumo_fuel')]//ul[@class='options']//label[normalize-space(text())='{option_name}']")
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label)
    time.sleep(1)

    checkbox_span = option_label.find_element(By.XPATH, "./preceding-sibling::span")
    driver.execute_script("arguments[0].click();", checkbox_span)
    time.sleep(1)


    caption_label = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_fuel > p.CaptionCont.SelectBox")))
    wait.until(lambda d: option_name in caption_label.text)
    caption_label.click()
    time.sleep(1)

    region_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_region .SelectBox")))
    region_dropdown.click()
    time.sleep(2)


    vojvodina_label = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         "//div[contains(@class,'sumo_region')]//ul[@class='options']//label[normalize-space(text())='Vojvodina']")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", vojvodina_label)
    time.sleep(2)


    checkbox_span = vojvodina_label.find_element(By.XPATH, "./preceding-sibling::span")
    driver.execute_script("arguments[0].click();", checkbox_span)
    time.sleep(2)


    caption_label = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_region > p.CaptionCont.SelectBox")))
    wait.until(lambda d: "Vojvodina" in caption_label.text)
    caption_label.click()
    time.sleep(2)


    driver.find_element(By.CSS_SELECTOR, ".sumo_showOldNew .SelectBox").click()
    time.sleep(2)
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'sumo_showOldNew')]//li[label[text()='Samo polovna vozila']]").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[contains(text(), 'PRETRAGA')]").click()

    arteon_title=driver.find_element(By.TAG_NAME,"h1").text
    assert "Volkswagen Arteon od 2017 do 2024 - Cena do 30000€" in arteon_title,"Error"

def test_polovni_automobili_search_harley_davidson_sportster_(driver):
        accept_cookies(driver)
        wait = WebDriverWait(driver, 50)

        motori_link = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//a[@href="/motori" and contains(@class, "table-cell")]')))

        actions = ActionChains(driver)

        actions.move_to_element(motori_link).click().perform()
        dropdown_trigger = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.SumoSelect[name='brand'], div.SumoSelect"))
        )
        dropdown_trigger.click()
        time.sleep(2)

        search_input = driver.find_element(By.CSS_SELECTOR, ".SumoSelect.open input")
        search_input.send_keys("Harley Davidson")
        time.sleep(2)

        harley_davidson_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Harley Davidson')]")))
        harley_davidson_option.click()
        time.sleep(3)

        #     II modeli

        search_input = driver.find_element(By.ID, "modeltxt")
        search_input.send_keys("Sportster")
        time.sleep(2)

        #     III CENA DO
        driver.find_element(By.ID, "price_to").send_keys("10000")
        time.sleep(2)

        #     IV Godiste od
        year_value_from = "2000"
        year_label_from = f"{year_value_from} god."

        year_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_year_from .SelectBox")))
        year_dropdown.click()
        time.sleep(3)

        option_label_from = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             f"//div[contains(@class,'sumo_year_from')]//ul[@class='options']//label[normalize-space(text())='{year_label_from}']")
        ))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label_from)
        option_label_from.click()
        time.sleep(2)

        #     V DO
        year_value_to = "2024"
        year_label_to = f"{year_value_to} god."

        year_dropdown_to = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_year_to .SelectBox")))
        year_dropdown_to.click()
        time.sleep(3)

        option_label_to = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             f"//div[contains(@class,'sumo_year_to')]//ul[@class='options']//label[normalize-space(text())='{year_label_to}']")
        ))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label_to)
        option_label_to.click()
        time.sleep(2)

        caption_label_to = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_year_to > p.CaptionCont.SelectBox")))
        wait.until(lambda d: year_value_to in caption_label_to.text)
        time.sleep(2)

        #     VI tip

        type_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_type .SelectBox")))
        type_dropdown.click()
        time.sleep(3)

        option_name = "Chopper / Cruiser"

        option_label = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             f"//div[contains(@class,'sumo_type')]//ul[@class='options']//label[normalize-space(text())='{option_name}']")
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", option_label)
        time.sleep(2)

        checkbox_span = option_label.find_element(By.XPATH, "./preceding-sibling::span")
        driver.execute_script("arguments[0].click();", checkbox_span)
        time.sleep(2)

        caption_label = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".sumo_type > p.CaptionCont.SelectBox")))
        wait.until(lambda d: option_name in caption_label.text)

        caption_label.click()

        time.sleep(2)

        # VII REG
        region_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sumo_region .SelectBox")))
        region_dropdown.click()
        time.sleep(2)

        bgd_label = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             "//div[contains(@class,'sumo_region')]//ul[@class='options']//label[normalize-space(text())='Beograd']")
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", bgd_label)
        time.sleep(2)

        checkbox_span = bgd_label.find_element(By.XPATH, "./preceding-sibling::span")
        driver.execute_script("arguments[0].click();", checkbox_span)
        time.sleep(2)

        #     VII pol

        driver.find_element(By.CSS_SELECTOR, ".sumo_showOldNew .SelectBox").click()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "//div[contains(@class,'sumo_showOldNew')]//li[label[text()='Samo polovne motore']]").click()
        time.sleep(2)

        driver.find_element(By.XPATH, "//button[contains(text(), 'PRETRAGA')]").click()

        harley_title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        assert "Harley Davidson Sportster od 2000 do 2024 - Cena do 10000€" in harley_title, "Error"

def test_polovni_automobili_click_popular_models(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    najtrazeniji_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//section//h3/a[text()='Najtraženiji modeli']")
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", najtrazeniji_link)
    time.sleep(0.3)

    najtrazeniji_link.click()

    popular_models_title=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Najtraženiji modeli automobila" in popular_models_title, "Error"

def test_polovni_automobili_click_about_us_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 10)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # sačekaj da se footer elementi učitaju

    o_nama_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "O nama")))

    o_nama_link.click()

    o_nama_text=driver.find_element(By.TAG_NAME,"h1").text
    assert "O sajtu Polovniautomobili.com" in o_nama_text,"Error"

def test_polovni_automobili_click_mobile_applications_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 10)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    mobile_applications_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Mobilne aplikacije")))

    mobile_applications_link.click()

    mobile_applications_title = driver.find_element(By.TAG_NAME, "h1").text
    assert "Mobilne aplikacije" in mobile_applications_title, "Error"

def test_polovni_automobili_click_poslovi_infostud_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    poslovi_logo = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "img[alt='poslovi infostud logo']")
    ))

    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", poslovi_logo)

    link_element = driver.execute_script("return arguments[0].closest('a');", poslovi_logo)
    driver.execute_script("arguments[0].click();", link_element)

    wait.until(lambda driver: len(driver.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])  #


    infostud_title=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Najveći izbor oglasa za posao na jednom mestu" in infostud_title, "Error"

def test_polovni_automobili_logout(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login(driver)

    moj_profil = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a.js_ga-event.signin_menu_element[data-label='klik na moj profil']")
    ))

    # Napravi akciju hover (mouse over)
    actions = ActionChains(driver)
    actions.move_to_element(moj_profil).perform()

    # Sačekaj da se pojavi link za odjavu
    odjavi_se = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.js-logout-link.signin_menu_element[title='Odjavite se iz sistema']")
    ))

    # Klikni na "Odjavi se"
    odjavi_se.click()







