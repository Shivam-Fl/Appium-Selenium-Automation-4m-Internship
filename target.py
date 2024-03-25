import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string


def generate_random_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def TargetSignIn(email_or_username):
    # Start the WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.target.com/")

    try:
        # Click on the first Sign in button
        first_signin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Sign in")]')))
        first_signin_button.click()
        time.sleep(1)
        # Wait for the modal to appear and click on the second Sign in button
        second_signin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-test="accountNav-signIn"]/span')))
        second_signin_button.click()

        # Enter email/username
        email_username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]')))
        email_username_input.clear()
        email_username_input.send_keys(email_or_username)

        # Generate a random password and enter it
        password = generate_random_password()
        password_input = driver.find_element(By.XPATH, '//input[@id="password"]')
        password_input.send_keys(password)

        # Click on Sign in with password button
        signin_button = driver.find_element(By.XPATH, '//span[contains(text(), "Sign in with password")]')
        signin_button.click()

        # Check for error message
        try:
            try:
                error_message = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "That password is incorrect.")]')))
                if error_message:
                    return {"User Registered": True}
            except:
                error_message1 = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Your account is locked. Please click on forgot password link to reset.")]')))

                if error_message1:
                    return {"User Registered": True}
        except:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "We can\'t find your account.")]')))
            if error_message:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()



email_or_number = input("Enter email or phone: ") 
result = TargetSignIn(email_or_number)
print(result)
