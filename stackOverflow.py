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


def automate_stack_overflow(email):
    driver = webdriver.Chrome()
    driver.get("https://stackoverflow.com/users/login")

    try:
        # Enter email
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='email']"))
        )
        email_input.send_keys(email)

        # Generate a random password
        password = generate_random_password()

        # Enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='password']"))
        )
        password_input.send_keys(password)

        # Click on the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='submit-button']"))
        )
        login_button.click()

        # Check for error message
        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(), 'The email or password is incorrect.')]"))
            )
            if error_message:
                return {"User Registered": True}
        except:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(), 'No user found with matching email')]"))
            )
            if error_message:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


# Test the function
email = input("Enter your email: ")
result = automate_stack_overflow(email)
print(result)
