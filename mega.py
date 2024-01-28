import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def MegaRecovery(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://mega.nz/recovery')

    try:
        time.sleep(10)
        wait = WebDriverWait(driver, 10)

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="recover-input1"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on the Start span
        start_span = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Start")]')))
        start_span.click()

        try:
            # Try to find an h1 with text "Do you have a backup of your recovery key?"
            h1_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//h1[@class="step-main-question" and contains(text(), "Do you have a backup of your recovery key?")]')))

            # If the h1 element is found, user registration succeeded
            if h1_element:
                return {"User Registered": True}

        except:
            # Expect for a div with specific text
            error_div = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Email address not found, please try again. If you cannot remember the email address associated with your MEGA account, clear the input field and click Start again to skip this step.")]')))

            # If the error div is found, user registration failed
            if error_div:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    recovery_result = MegaRecovery(email)
    print(recovery_result)
