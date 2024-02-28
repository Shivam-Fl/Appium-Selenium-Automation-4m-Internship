from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint

def generate_password():
    # Generate a random password with 8 characters
    password = ''.join(chr(randint(33, 126)) for _ in range(8))
    return password

def PariMatchRegister(phone):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://pari-match-bet.in/en/login')

    try:
        wait = WebDriverWait(driver, 10)

        # Enter phone number
        phone_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-testid="phone-field-input"]')))
        phone_input.clear()
        phone_input.send_keys(phone)

        # Generate and enter random password
        password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-testid="password-field-input"]')))
        password = generate_password()
        password_input.clear()
        password_input.send_keys(password)

        # Click on the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
        login_button.click()

        # Check for error message
        error_message = wait.until(EC.visibility_of_element_located((By.XPATH, '//h2[@data-testid="error-alert-title"]')))
        if "Incorrect password" in error_message.text:
            return {"User Registered": True}
        elif "Seems you entered incorrect data" in error_message.text:
            return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    phone = input("Enter your phone number: ")
    registration_result = PariMatchRegister(phone)
    print(registration_result)
