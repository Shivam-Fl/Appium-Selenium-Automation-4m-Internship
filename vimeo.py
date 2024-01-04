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

def generate_random_password():
    # Ensure password is at least 8 characters long and contains at least one number and one symbol
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for _ in range(8))
        if any(char.isdigit() for char in password) and any(char in string.punctuation for char in password):
            return password

def VimeoSignUp(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://vimeo.com/join')

    try:
        wait = WebDriverWait(driver, 10)

        # Generate meaningful name
        meaningful_name = generate_meaningful_word(10)

        # Generate random password
        random_password = generate_random_password()

        # Input email
        email_input = wait.until(EC.presence_of_element_located((By.ID, 'signup_email')))
        email_input.clear()
        email_input.send_keys(email)

        # Input meaningful name
        full_name_input = driver.find_element(By.ID, 'signup_name')
        full_name_input.clear()
        full_name_input.send_keys(meaningful_name)

        # Input random password
        password_input = driver.find_element(By.ID, 'signup_password')
        password_input.clear()
        password_input.send_keys(random_password)

        # Click the "Join with email" button
        submit_button = driver.find_element(By.XPATH, '//input[@value="Join with email"]')
        submit_button.click()

        try:
            # Check if the "Hey, we recognize this email!" div is present
            error_message = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(text(), "Hey, we recognize this email!")]')))
            if error_message:
                return {"User Exists": True, "Message": "Hey, we recognize this email!"}

        except:
            # Check if the URL changes
            welcome_text = ((wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//h2[contains(text(), "What brings you to Vimeo?")]'))) or
                            wait.until(EC.visibility_of_element_located((By.XPATH, '//h2[contains(text(), "How do you use Vimeo?")]')))) or
                            wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), "Get started with a free trial of Vimeo Standard")]'))))
            if welcome_text:
                return {"User Exists": False}

    except Exception as e:
        print("Element not found", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    email_input = input("Enter a Vimeo email: ")

    message = VimeoSignUp(email_input)
    print(message)
