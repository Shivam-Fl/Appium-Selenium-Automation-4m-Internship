from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

def generate_meaningful_word(length):
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    word = ''.join(random.choice(consonants) + random.choice(vowels) for _ in range(length // 2))
    return word.capitalize()

def generate_random_username(length):
    allowed_characters = string.ascii_letters + string.digits + '_.'
    return ''.join(random.choice(allowed_characters) for _ in range(length))

def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def InstagramSignUp(emailOrPhone):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.instagram.com/accounts/emailsignup/')

    try:
        wait = WebDriverWait(driver, 10)

        # Generate meaningful name
        meaningful_name = generate_meaningful_word(10)

        # Generate random username and password
        random_username = generate_random_username(10)
        random_password = generate_random_password(10)

        # Input email or phone number
        email_phone_input = wait.until(EC.presence_of_element_located((By.NAME, 'emailOrPhone')))
        email_phone_input.clear()
        email_phone_input.send_keys(emailOrPhone)

        # Input meaningful name
        full_name_input = driver.find_element(By.NAME, 'fullName')
        full_name_input.clear()
        full_name_input.send_keys(meaningful_name)

        # Input random username
        username_input = driver.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(random_username)

        # Input random password
        password_input = driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(random_password)

        # Click the "Sign Up" button
        submit_button = driver.find_element(By.XPATH, '//button[contains(text(), "Sign up")]')
        submit_button.click()

        try:
            # Check if the error message is present
            error_message = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//p[@role="alert" and contains(text(), "Another account is using the same email")]')))
            if error_message:
                return {"User Exists": True, "Message": "Another account is using the same email"}

        except:
            # Check if the "Next" button is present
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Next")]')))
            if next_button:
                return {"User Exists": False, "Message": "User not registered, click 'Next' to proceed"}

    except Exception as e:
        print("Element not found", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    email_phoneNum = input("Enter an Instagram email or phone number: ")

    message = InstagramSignUp(email_phoneNum)
    print(message)
