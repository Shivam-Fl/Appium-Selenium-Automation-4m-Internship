
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def BBCLogin(input_email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(
        'https://account.bbc.com/signin')

    try:
        wait = WebDriverWait(driver, 10)

        email_input = wait.until(EC.presence_of_element_located((By.ID, 'user-identifier-input')))
        email_input.clear()
        email_input.send_keys(input_email)

        next_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit-button')))
        next_button.click()

        try:
            error_message = wait.until(EC.visibility_of_element_located((By.ID, 'form-message-general'))).text
            if "We don’t recognise that email or username" in error_message:
                return {"User Registered": False}
        except:
            password_input = wait.until(EC.presence_of_element_located((By.ID, 'password-input')))
            if password_input:
                return {"User Registered": True}
    except Exception as e:
        print("Element not found", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter an email you want to find: ")
    message = BBCLogin(email)
    print(message)
