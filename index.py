import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import logging
import random

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize undetected_chromedriver with stealth mode
options = uc.ChromeOptions()
options.headless = False  # For debugging, set to True for headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--disable-web-security')
options.add_argument('--incognito')

# Add additional headers to mimic a real user
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = uc.Chrome(options=options)

# Apply stealth settings to avoid detection
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def random_delay():
    time.sleep(random.uniform(1, 3))

def continuously_inject_js():
    script = """
        // Disable navigator.webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Remove anti-automation scripts
        const scripts = document.querySelectorAll('script');
        scripts.forEach(script => {
            if (script.innerHTML.includes('anti-automation')) {
                script.parentNode.removeChild(script);
            }
        });

        // Disable setInterval and setTimeout for certain functions
        window.setInterval = (func, delay) => {
            if (func.toString().includes('anti-automation')) {
                return null;
            }
            return setInterval(func, delay);
        };

        window.setTimeout = (func, delay) => {
            if (func.toString().includes('anti-automation')) {
                return null;
            }
            return setTimeout(func, delay);
        };
    """
    try:
        while True:
            driver.execute_script(script)
            time.sleep(1)
    except Exception as e:
        logging.error('Error in continuously injecting JS: %s', e)

def login(username, password):
    logging.info('Opening SmartPLAY login page')
    driver.get('https://www.smartplay.lcsd.gov.hk/home')
    
    # Start the continuous JavaScript injection in a separate thread
    import threading
    js_injection_thread = threading.Thread(target=continuously_inject_js)
    js_injection_thread.daemon = True
    js_injection_thread.start()

    try:
        logging.info('Waiting for login form to appear')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'pc-login-username'))
        )
    except Exception as e:
        logging.error('Error while waiting for login form: %s', e)
        driver.save_screenshot('error_waiting_login_form.png')
        driver.quit()
        return

    try:
        logging.info('Entering username')
        username_field = driver.find_element(By.NAME, 'pc-login-username')
        username_field.click()
        random_delay()
        username_field.send_keys(username)
        
        logging.info('Entering password')
        password_field = driver.find_element(By.NAME, 'pc-login-password')
        password_field.click()
        random_delay()
        password_field.send_keys(password)
    except Exception as e:
        logging.error('Error while entering login credentials: %s', e)
        driver.save_screenshot('error_entering_credentials.png')
        driver.quit()
        return

    try:
        logging.info('Clicking login button')
        login_button = driver.find_element(By.XPATH, '//div[@name="pc-login-btn"]//div[contains(text(), "登錄")]')
        login_button.click()
        
        # Adding a wait to ensure login completes
        logging.info('Waiting for facility menu item to appear')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="button"]//span[contains(text(), "設施")]'))
        )
        logging.info('Login successful')
    except Exception as e:
        logging.error('Error during login process: %s', e)
        driver.save_screenshot('error_during_login.png')
        driver.quit()
        return

def navigate_to_facility():
    try:
        logging.info('Waiting for facility menu item to appear')
        facility_menu_item = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@role="button"]//span[contains(text(), "設施")]'))
        )
        
        logging.info('Clicking facility menu item')
        random_delay()
        facility_menu_item.click()
        logging.info('Navigated to facility page')
    except Exception as e:
        logging.error('Error while navigating to facility: %s', e)
        driver.save_screenshot('error_navigating_facility.png')
        driver.quit()
        return

def book_venue(date, time, venue):
    navigate_to_facility()

    try:
        logging.info('Waiting for booking page to load')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'bookingDate'))
        )

        logging.info('Entering booking date')
        random_delay()
        driver.find_element(By.ID, 'bookingDate').send_keys(date)
        
        logging.info('Entering booking time')
        random_delay()
        driver.find_element(By.ID, 'bookingTime').send_keys(time)
        
        logging.info('Entering booking venue')
        random_delay()
        driver.find_element(By.ID, 'bookingVenue').send_keys(venue)

        logging.info('Submitting booking form')
        random_delay()
        driver.find_element(By.XPATH, '//button[contains(text(), "提交预订")]').click()
    except Exception as e:
        logging.error('Error during booking process: %s', e)
        driver.save_screenshot('error_during_booking.png')
        driver.quit()
        return

# Example usage
username = 'moterial'
password = 'Q@bgJf67R'
date = '2024-07-10'
time = '10:00'
venue = '某体育馆'

logging.info('Starting booking process')
try:
    login(username, password)
    book_venue(date, time, venue)
except Exception as e:
    logging.error('An error occurred: %s', e)
finally:
    logging.info('Booking process completed, closing browser')
    driver.quit()
