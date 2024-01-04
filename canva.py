from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def CanvaSignUp(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.canva.com/')

    try:
        wait = WebDriverWait(driver, 10)

        # Click the "Log in" button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Log in"]')))
        login_button.click()

        # Click the "Continue with email" button
        continue_with_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Continue with email"]')))
        continue_with_email_button.click()

        # Input email
        email_input = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        email_input.clear()
        email_input.send_keys(email)
        continue_button = driver.find_element(By.XPATH, '//button[@type="submit" and .//span[text()="Continue"]]')
        continue_button.click()
        driver.implicitly_wait(5)

        try:
            code_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//h2[contains(text(), "Didn\'t get the code ?")]')))
            if code_button:
                return {"User Exists": True, "Message": "User already registered"}
        except:
            pass

        # Try to find "Create your account" button
        try:
            create_account_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and .//span[text()="Create your account"]]')))
            if create_account_button:
                return {"User Exists": False, "Message": "User not registered"}
        except:
            pass

    except Exception as e:
        print("Element not found", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    email_address = input("Enter your Canva email: ")

    message = CanvaSignUp(email_address)
    print(message)
