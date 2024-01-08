import string
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def MailchimpLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://login.mailchimp.com/')

    try:
        wait = WebDriverWait(driver, 10)

        # Find and enter email
        email_input = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        email_input.clear()
        email_input.send_keys(email)

        # Find and enter a random password
        password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        generated_password = generate_random_password()
        password_input.clear()
        password_input.send_keys(generated_password)

        try:
            captcha_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'recaptcha-checkbox-checkmark')))
            captcha_button.click()

        except:
            pass

        # Click on "Login" button
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Log in")]')))
        login_button.click()

        try:
            # Check if the error message for incorrect username is present
            username_error_message = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//p[contains(text(), "Sorry, we couldn\'t find an account with that username.")]')))

            # If the message is found, user is not registered
            if username_error_message:
                return {"User Registered": False}


        except:
            password_error_message = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[contains(text(), "Sorry, that password isn\'t right. We can help you")]')))

            if password_error_message:
                return {"User Registered": True}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter a Mailchimp email: ")
    message = MailchimpLogin(email)
    print(message)
