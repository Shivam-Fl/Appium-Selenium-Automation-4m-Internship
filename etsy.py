from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string


def generate_random_password(length):
    # Generate a random password with letters and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def automate_etsy(email):
    driver = webdriver.Chrome()
    driver.get("https://www.etsy.com/")

    try:
        # Click on the Sign in button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'signin-header-action') and contains(text(), 'Sign in')]")))
        sign_in_button.click()

        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='join_neu_email_field']")))
        email_field.send_keys(email)

        # Generate a random password
        password = generate_random_password(8)

        # Enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='join_neu_password_field']")))
        password_field.send_keys(password)

        # Click on the sign in button
        sign_in_submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='submit_attempt' and contains(text(), 'Sign in')]")))
        sign_in_submit_button.click()

        # Check for password error message
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                   "//div[contains(text(), 'Password was incorrect')]")))
            return {"User registered": True}
        except:
            WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                       "//div[contains(text(), 'Email address is invalid.')]")))
            return {"User registered": False}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter your email: ")
    result = automate_etsy(email)
    print(result)
