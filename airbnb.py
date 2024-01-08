from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import the Options class
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def AirbnbLogin(email):
    chrome_options = Options()  # Create an instance of the Options class
    chrome_options.add_argument("--headless")  # Add the headless option

    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://www.airbnb.co.in/login')

    try:
        wait = WebDriverWait(driver, 7)

        # Find and click "Continue with email"
        continue_with_email_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Continue with email")]')))
        continue_with_email_button.click()

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="email-login-email"]')))
        email_input.clear()
        email_input.send_keys(email)

        continue_span = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@data-testid="signup-login-submit-btn"]')))
        continue_span.click()

        try:
            # Check if the password input is present
            password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-testid="forgot-password-link"]')))

            # If password input is found, user is registered
            if password_input:
                return {"User Registered": True}

        except:
            # Check for "Agree and Continue" span
            agree_and_continue_span = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Agree and continue")]')))

            # If "Agree and Continue" span is found, user is not registered
            if agree_and_continue_span:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter an Airbnb email: ")
    message = AirbnbLogin(email)
    print(message)
