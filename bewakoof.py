from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def BewakoofLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.bewakoof.com/login')

    try:
        wait = WebDriverWait(driver, 10)

        # Click on the email login button
        email_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="web_email_login"]')))
        email_login_button.click()

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="email_input"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Generate and enter random password
        password = generate_random_password()
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="mob_password"]')))
        password_input.clear()
        password_input.send_keys(password)

        # Click on the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="mob_login_password_submit"]')))
        login_button.click()

        try:
            # Try to find a span with text "Incorrect login details. Please try again."
            error_span = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Incorrect login details. Please try again.")]')))

            # If the error span is found, login failed
            if error_span:
                return {"User Registered": True}

        except:
            # Expect for a span with text "API internal error: undefined method `id' for nil:NilClass"
            api_error_span = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "API internal error: undefined method `id\' for nil:NilClass")]')))

            # If the API error span is found, login failed
            if api_error_span:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    login_result = BewakoofLogin(email)
    print(login_result)
