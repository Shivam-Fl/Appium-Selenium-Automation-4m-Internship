from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
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


def generate_random_name():
    fake = Faker()
    return fake.name()


def UdemyRegister(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.udemy.com/join/signup-popup/')

    try:
        wait = WebDriverWait(driver, 10)

        # Generate a random meaningful name
        name = generate_random_name()

        # Add a random meaningful name to input with id "form-group--1"
        name_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="form-group--1"]')))
        name_input.clear()
        name_input.send_keys(name)

        # Add email to input with id "form-group--3"
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="form-group--3"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Generate a random password
        password = generate_random_password()

        # Add password to input with id "form-group--5"
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="form-group--5"]')))
        password_input.clear()
        password_input.send_keys(password)

        # Click on span with text "Sign up"
        sign_up_span = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Sign up"]')))
        sign_up_span.click()

        try:
            # Try to find a div with text "There was a problem creating your account. Check that your email address is spelled correctly."
            error_div = wait.until(
                EC.visibility_of_element_located((By.XPATH,
                                                  '//div[text()="There was a problem creating your account. Check that your email address is spelled correctly."]')))

            # If the error div is found, user registration failed
            if error_div:
                return {"User Registered": True}

        except:
            # Expect for a tag with href "/user/edit-profile/"
            edit_profile_link = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//a[@href="/user/edit-profile/"]')))

            # If the edit profile link is found, user registration succeeded
            if edit_profile_link:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
        
    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = UdemyRegister(email)
    print(registration_result)
