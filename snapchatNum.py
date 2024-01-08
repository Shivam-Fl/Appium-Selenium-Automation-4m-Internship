from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def SnapchatLogin(phone_number):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://accounts.snapchat.com/accounts/v2/login')

    try:
        wait = WebDriverWait(driver, 5)

        # Find and click on "Use phone number instead"
        use_phone_number_instead = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Use phone number instead")]')))
        use_phone_number_instead.click()

        # Select country code 91 (India)
        country_code_select = wait.until(
            EC.element_to_be_clickable((By.NAME, 'accountIdentifierCountryCode')))
        country_code_select.click()
        country_code_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//option[@value="91"]')))
        country_code_option.click()

        # Enter phone number
        phone_number_input = wait.until(
            EC.presence_of_element_located((By.NAME, 'accountIdentifierPhoneNumber')))
        phone_number_input.clear()
        phone_number_input.send_keys(phone_number)

        # Click on "Next" button
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Next")]')))
        next_button.click()

        try:
            # Check if the h1 tag with text "Enter password" is present
            enter_password_heading = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Enter Password")]')))

            # If the heading is found, user is registered
            if enter_password_heading:
                return {"User Registered": True}

        except:
            # Check for the p tag with text "We cannot find an account for this phone number."
            account_not_found_message = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//p[contains(text(), "We cannot find an account for this phone number.")]')))

            # If the message is found, user is not registered
            if account_not_found_message:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    phone_number = input("Enter a Snapchat phone number: ")
    message = SnapchatLogin(phone_number)
    print(message)
