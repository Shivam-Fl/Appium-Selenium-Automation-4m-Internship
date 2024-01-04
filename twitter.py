from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def TwitterLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://twitter.com/i/flow/login')

    try:
        wait = WebDriverWait(driver, 10)

        # Check if the username input is present
        username_input = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
        username_input.clear()
        username_input.send_keys(email)

        # Click the "Next" button using a flexible XPath
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]')))
        next_button.click()

        try:
            # Check if the error message is present
            error_message = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Sorry, we could not find your account")]')))
            if error_message:
                return {"User Exists": False}

        except:
            # Check if the password input is present
            password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
            if password_input:
                return {"User Exists": True}

    except Exception as e:
        print("Element not found", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    email_phoneNum = input("Enter a Twitter username: ")
    message = TwitterLogin(email_phoneNum)
    print(message)
