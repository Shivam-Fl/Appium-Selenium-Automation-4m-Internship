from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def DropboxLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.dropbox.com/login')

    try:
        wait = WebDriverWait(driver, 10)

        # Find the email input field using Xpath
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on "Continue" span using Xpath
        continue_span = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Continue"]')))
        continue_span.click()

        try:
            # Check for the span with text "Welcome back" using Xpath
            welcome_back_span = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//span[text()="Welcome back"]')))
            
            # If the welcome back span is found, user is registered
            if welcome_back_span:
                return {"User Registered": True}

        except:
            # Check for the span with text "Sign up for free" using Xpath
            sign_up_span = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//span[text()="Sign up for free"]')))

            # If the sign up span is found, user is not registered
            if sign_up_span:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
        

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your Dropbox email: ")
    login_result = DropboxLogin(email)
    print(login_result)
