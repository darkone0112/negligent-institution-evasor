import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import getpass
from selenium.webdriver.common.action_chains import ActionChains
import requests
from datetime import datetime, timedelta
import json
import os
import sys

def load_config():
    try:
        # Get the directory where the executable/script is located
        if getattr(sys, 'frozen', False):
            # If frozen (exe), use sys._MEIPASS
            base_path = os.path.dirname(sys.executable)
        else:
            # If script, use script directory
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        config_path = os.path.join(base_path, 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config['personal_info']
    except FileNotFoundError:
        print("Error: config.json not found. Please create it with your personal information.")
        input("Press Enter to exit...")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON. Please check the format.")
        input("Press Enter to exit...")
        sys.exit(1)
    except KeyError:
        print("Error: config.json is missing required 'personal_info' section.")
        input("Press Enter to exit...")
        sys.exit(1)

def get_wait_time():
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_second = now.second
    
    # Default wait time is 5 minutes
    wait_seconds = 300  # 5 minutes
    
    # If we're between 12 and 18
    if 12 <= current_hour <= 18:
        # Calculate time until next hour
        minutes_to_next_hour = 59 - current_minute
        seconds_to_next_minute = 60 - current_second
        seconds_to_next_hour = minutes_to_next_hour * 60 + seconds_to_next_minute
        
        # If we're within 6 minutes of the next hour
        if seconds_to_next_hour <= 360:  # 6 minutes
            # Wait until 20 seconds before the next hour
            wait_seconds = seconds_to_next_hour - 20
            if wait_seconds < 0:  # If we're past the 20-second mark
                wait_seconds = 300  # Wait 5 minutes
        
    next_run = datetime.now() + timedelta(seconds=wait_seconds)
    print(f"Next attempt scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    return wait_seconds

# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

PROXY_LIST_URL = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

def get_random_proxy():
    try:
        response = requests.get(PROXY_LIST_URL, timeout=10)
        proxies = [line.strip() for line in response.text.splitlines() if line.strip() and line.startswith('http')]
        if proxies:
            return random.choice(proxies).replace('http://', '')
    except Exception as e:
        print(f"Could not fetch proxy list: {e}")
    return None

def run_appointment_flow(use_proxy=False, proxy=None, existing_driver=None):
    if existing_driver:
        driver = existing_driver
    else:
        # Set up Chrome options
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
        chrome_options.add_argument("--lang=es-ES")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    if use_proxy and proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    if not existing_driver:
        driver = uc.Chrome(options=chrome_options)
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 20)

    def human_delay(a=0.8, b=2.0):
        time.sleep(random.uniform(a, b))

    def scroll_to_element(driver, element):
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        human_delay(0.5, 1.2)

    def move_mouse_to_element(element):
        actions.move_to_element(element).perform()
        human_delay(0.3, 0.8)

    def human_type(element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.18))

    try:
        # Start at the new URL
        start_url = "https://sede.administracionespublicas.gob.es/pagina/index/directorio/icpplus"
        driver.get(start_url)
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected on initial load")
        driver.execute_script(f"Object.defineProperty(document, 'referrer', {{get: () => '{start_url}'}});")

        # Click the 'Acceder al Procedimiento' button
        acceder_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        scroll_to_element(driver, acceder_btn)
        move_mouse_to_element(acceder_btn)
        human_delay(0.7, 1.5)
        acceder_btn.click()
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected after acceder_btn click")

        # Province dropdown
        select_element = wait.until(EC.presence_of_element_located((By.ID, "form")))
        scroll_to_element(driver, select_element)
        move_mouse_to_element(select_element)
        select = Select(select_element)
        human_delay(0.5, 1.2)
        select.select_by_visible_text("Madrid")
        human_delay(1.0, 2.0)

        accept_button = wait.until(EC.element_to_be_clickable((By.ID, "btnAceptar")))
        scroll_to_element(driver, accept_button)
        move_mouse_to_element(accept_button)
        human_delay(0.7, 1.5)
        accept_button.click()
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected after first aceptar click")

        # 'sede' dropdown
        sede_select = wait.until(EC.presence_of_element_located((By.ID, "sede")))
        scroll_to_element(driver, sede_select)
        move_mouse_to_element(sede_select)
        sede = Select(sede_select)
        human_delay(0.5, 1.2)
        sede.select_by_visible_text("Cualquier oficina")
        human_delay(1.0, 2.0)

        # 'tramite' dropdown
        tramite_select = wait.until(EC.presence_of_element_located((By.ID, "tramiteGrupo[0]")))
        scroll_to_element(driver, tramite_select)
        move_mouse_to_element(tramite_select)
        tramite = Select(tramite_select)
        human_delay(0.5, 1.2)
        tramite.select_by_visible_text("POLICÍA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) INICIAL, RENOVACIÓN, DUPLICADO Y LEY 14/2013")
        human_delay(1.0, 2.0)

        # 'Aceptar' button
        accept_button2 = wait.until(EC.element_to_be_clickable((By.ID, "btnAceptar")))
        scroll_to_element(driver, accept_button2)
        move_mouse_to_element(accept_button2)
        human_delay(0.7, 1.5)
        accept_button2.click()
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected after second aceptar click")

        # 'Presentación sin Cl@ve' button
        btn_entrar = wait.until(EC.element_to_be_clickable((By.ID, "btnEntrar")))
        scroll_to_element(driver, btn_entrar)
        move_mouse_to_element(btn_entrar)
        human_delay(0.7, 1.5)
        btn_entrar.click()
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected after btnEntrar click")

        try:
            cookie_bar = driver.find_element(By.ID, "cookie-law-info-bar")
            accept_buttons = cookie_bar.find_elements(By.TAG_NAME, "button")
            for btn in accept_buttons:
                if btn.is_displayed() and btn.is_enabled():
                    move_mouse_to_element(btn)
                    btn.click()
                    break
            driver.execute_script("arguments[0].style.display = 'none';", cookie_bar)
        except Exception as e:
            pass

        # NIE
        nie_input = wait.until(EC.presence_of_element_located((By.ID, "txtIdCitado")))
        scroll_to_element(driver, nie_input)
        move_mouse_to_element(nie_input)
        human_delay(0.5, 1.2)
        # Load personal information from config
        personal_info = load_config()
        
        nie_input.clear()
        human_type(nie_input, personal_info['nie'])
        human_delay(0.7, 1.5)

        # Name
        name_input = wait.until(EC.presence_of_element_located((By.ID, "txtDesCitado")))
        scroll_to_element(driver, name_input)
        move_mouse_to_element(name_input)
        human_delay(0.5, 1.2)
        name_input.clear()
        full_name = f"{personal_info['name']} {personal_info['surname']}"
        human_type(name_input, full_name)
        human_delay(0.7, 1.5)

        # Nationality
        nat_select = wait.until(EC.presence_of_element_located((By.ID, "txtPaisNac")))
        scroll_to_element(driver, nat_select)
        move_mouse_to_element(nat_select)
        human_delay(0.5, 1.2)
        nat = Select(nat_select)
        nat.select_by_visible_text(personal_info['nationality'])
        human_delay(1.0, 2.0)

        # 'Aceptar' button
        btn_enviar = wait.until(EC.element_to_be_clickable((By.ID, "btnEnviar")))
        scroll_to_element(driver, btn_enviar)
        move_mouse_to_element(btn_enviar)
        human_delay(0.7, 1.5)
        btn_enviar.click()
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected after NIE form submit")

        # 'Solicitar Cita' button (final step)
        solicitar_cita_btn = wait.until(
            lambda d: d.find_element(By.XPATH, "//input[@id='btnEnviar' and @value='Solicitar Cita']")
        )
        scroll_to_element(driver, solicitar_cita_btn)
        move_mouse_to_element(solicitar_cita_btn)
        human_delay(0.7, 1.5)
        solicitar_cita_btn.click()
        human_delay(2.0, 3.0)
        if "demasiadas peticiones" in driver.page_source.lower() or "too many requests" in driver.page_source.lower():
            raise Exception("Too many requests detected after solicitar cita click")
            
        # Check for no appointments message
        if "no hay citas disponibles para la reserva sin cl@ve" in driver.page_source.lower():
            print("No appointments available without Cl@ve.")
            
            # Get appropriate wait time
            wait_seconds = get_wait_time()
            print(f"Waiting {wait_seconds/60:.1f} minutes...")
            
            time.sleep(wait_seconds)
            print("Refreshing and retrying...")
            try:
                driver.refresh()
                run_appointment_flow(use_proxy=use_proxy, proxy=proxy)  # Start a new flow
            except Exception as refresh_error:
                print(f"Error during refresh: {refresh_error}")
                # If refresh fails, start a new browser instance
                try:
                    driver.quit()
                except:
                    pass
                run_appointment_flow(use_proxy=use_proxy, proxy=proxy)
            return

        input("Script finished. You can now interact with the browser manually. Press Enter here to close the script (browser will remain open if you close it manually)...\n")
    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")
        try:
            driver.close()  # Close only current window instead of entire browser
        except:
            pass
            
        # Handle different types of errors
        if not error_message.strip():  # Empty error message (silent crash)
            print("Browser crashed or disconnected. Retrying...")
            wait_seconds = get_wait_time()
            print(f"Waiting {wait_seconds/60:.1f} minutes...")
            time.sleep(wait_seconds)
            run_appointment_flow(use_proxy=use_proxy, proxy=proxy)
            return
            
        if "demasiadas peticiones" in error_message.lower() or "too many requests" in error_message.lower():
            if not use_proxy:
                print("Retrying with a random proxy from ProxyScrape...")
                proxy = get_random_proxy()
                if proxy:
                    print(f"Using proxy: {proxy}")
                    wait_seconds = get_wait_time()
                    print(f"Waiting {wait_seconds/60:.1f} minutes...")
                    time.sleep(wait_seconds)
                    run_appointment_flow(use_proxy=True, proxy=proxy)
                    return
                else:
                    print("No proxy available.")
            else:
                print("Proxy failed or still blocked. Trying another proxy...")
                proxy = get_random_proxy()
                if proxy:
                    print(f"Using proxy: {proxy}")
                    wait_seconds = get_wait_time()
                    print(f"Waiting {wait_seconds/60:.1f} minutes...")
                    time.sleep(wait_seconds)
                    run_appointment_flow(use_proxy=True, proxy=proxy)
                    return
                else:
                    print("No proxy available.")
        
        # For any other error, wait and retry with same settings
        print("Retrying after error...")
        wait_seconds = get_wait_time()
        print(f"Waiting {wait_seconds/60:.1f} minutes...")
        time.sleep(wait_seconds)
        run_appointment_flow(use_proxy=use_proxy, proxy=proxy)
        return

# Run the flow
run_appointment_flow(use_proxy=False)
