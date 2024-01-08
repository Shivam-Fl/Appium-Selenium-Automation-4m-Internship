import string
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def PinterestLogin(email):
    chrome_options = Options()  # Create an instance of the Options class
    chrome_options.add_argument("--headless")  # Add the headless option

    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://in.pinterest.com/login/')

    try:
        wait = WebDriverWait(driver, 10)

        # Find and enter email
        email_input = wait.until(EC.presence_of_element_located((By.NAME, 'id')))
        email_input.clear()
        email_input.send_keys(email)

        # Find and enter password using the password generator
        password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        generated_password = generate_password()
        password_input.clear()
        password_input.send_keys(generated_password)

        # Find and click on "Login" div
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Log in")]')))
        login_button.click()

        try:
            # Check if the error message for incorrect email is present
            email_error_message = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[contains(text(), "The email you entered does not belong to any account.")]')))
            if email_error_message:
                return {"User Registered": False}

        except:
            # Check for the password error message
            password_error_message = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[contains(text(), "The password you entered is incorrect. Try again or")]')))

            # If password error message is found, user is registered
            if password_error_message:
                return {"User Registered": True}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter a Pinterest email: ")
    message = PinterestLogin(email)
    print(message)
