from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

def JeevansaathiLogin(phone_number):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.jeevansathi.com/')

    try:
        wait = WebDriverWait(driver, 10)

        # Click on "LOGIN" anchor tag
        login_anchor = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "LOGIN")]')))
        login_anchor.click()
        driver.implicitly_wait(5)

        # Enter a random password
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        password_input.clear()
        password_input.send_keys(random_password)

        # Enter phone number
        phone_input = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        phone_input.clear()
        phone_input.send_keys(phone_number)

        # Click on "Login" button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "LOGIN")]')))
        login_button.click()

        try:
            # Check for the error message "No profile exists for given email or phone"
            no_profile_message = wait.until(EC.visibility_of_element_located((By.XPATH,
                                  '//div[contains(text(), "No profile exists with given email or phone.")]')))

            # If the error message is found, user is not registered
            if no_profile_message:
                return {"User Registered": False}

        except:
            # Check for the error message "Login details provided were not correct"
            incorrect_login_message = wait.until(EC.visibility_of_element_located((By.XPATH,
                                          '//div[contains(text(), "Login details provided were not correct")]')))

            # If the error message is found, user is registered
            if incorrect_login_message:
                return {"User Registered": True}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    phone_number = input("Enter your phone number: ")
    login_result = JeevansaathiLogin(phone_number)
    print(login_result)
