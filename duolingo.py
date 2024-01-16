from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string


def generate_random_password(length=8):
    # Ensure at least one uppercase, one lowercase, and one digit
    uppercase_letter = random.choice(string.ascii_uppercase)
    lowercase_letter = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)

    # Combine characters
    characters = string.ascii_letters + string.digits + string.punctuation
    remaining_length = length - 3  # Subtract 3 for the uppercase, lowercase, and digit
    random_chars = ''.join(random.choice(characters) for i in range(remaining_length))

    # Shuffle and create the final password
    password = ''.join(random.sample(random_chars + uppercase_letter + lowercase_letter + digit, length))
    return password


def DuolingoRegister(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.duolingo.com/log-in')

    try:
        wait = WebDriverWait(driver, 10)

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-test="email-input"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Generate a random password
        password = generate_random_password()

        # Enter password
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-test="password-input"]')))
        password_input.clear()
        password_input.send_keys(password)

        # Click on the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-test="register-button"]')))
        login_button.click()

        try:
            # Try to find a div with text "Wrong password. Please try again."
            wrong_password_div = wait.until(
                EC.visibility_of_element_located((By.XPATH,
                                                  '//div[@data-test="invalid-form-field" and contains(text(), "Wrong password. Please try again.")]')))

            # If the wrong password div is found, user registration failed
            if wrong_password_div:
                return {"User Registered": True}

        except:
            # Expect for a div with text "There is no Duolingo account associated with 'email'. Please try again."
            no_account_div = wait.until(
                EC.visibility_of_element_located((By.XPATH,
                                                  f'//div[@data-test="invalid-form-field" and contains(text(), "There is no Duolingo account associated with")]')))

            # If the no account div is found, user registration succeeded
            if no_account_div:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)


    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = DuolingoRegister(email)
    print(registration_result)
