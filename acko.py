from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def AckoLogin(phone_number):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.acko.com/login')

    try:
        wait = WebDriverWait(driver, 10)

        # Click on "Recover my account" anchor tag
        recover_account_anchor = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Recover my account")]')))
        recover_account_anchor.click()

        # Find input with type text and enter phone number
        phone_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="text"]')))
        phone_input.clear()
        phone_input.send_keys(phone_number)

        # Click on "Continue" button
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continue")]')))
        continue_button.click()

        try:
            # Try to find a button with text "Send code"
            send_code_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Send Code")]')))

            # If the button is found, user is registered
            if send_code_button:
                return {"User Registered": True}

        except:
            # Try to find an h1 with text "No Account found"
            no_account_found_h1 = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), "No Account found")]')))

            # If the h1 is found, user is not registered
            if no_account_found_h1:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    phone_number = input("Enter your phone number: ")
    login_result = AckoLogin(phone_number)
    print(login_result)
