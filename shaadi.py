import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def ShaadiLogin(phone_number):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.shaadi.com/')

    try:
        wait = WebDriverWait(driver, 10)

        # Click on "Login" anchor tag
        login_anchor = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="login_link"]')))
        login_anchor.click()

        # Enter phone number
        phone_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="login_email"]')))
        phone_input.clear()
        phone_input.send_keys(phone_number)

        # Enter random password
        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-testid="login_password"]')))
        password_input.clear()
        random_password = generate_random_password()
        password_input.send_keys(random_password)

        # Click on "Sign In" button
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="sign_in"]')))
        sign_in_button.click()

        try:
            # Check for the error message "Please enter a valid password to Login"
            error_msg_password = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[@class="error_msg" and text()="Please enter a valid password to Login"]')))

            # If the error message is found, user is registered
            if error_msg_password:
                return {"User Registered": True}

        except:
            # Check for the error message "This Mobile No. is not registered with us"
            error_msg_phone = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[@class="error_msg" and text()="This Mobile No. is not registered with us"]')))

            # If the error message is found, user is not registered
            if error_msg_phone:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
        return {"User not found": True}

    finally:
        driver.quit()


if __name__ == "__main__":
    phone_number = input("Enter your phone number: ")
    login_result = ShaadiLogin(phone_number)
    print(login_result)
