from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def AWSLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://aws.amazon.com/console/')

    try:
        # Find and click on the "Sign In" link
        sign_in_link = driver.find_element(By.LINK_TEXT, 'Sign In')
        sign_in_link.click()

        # Enter email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="resolving_input"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on "Next"
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]')))
        next_button.click()

        try:
            # Check for error message
            error_title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//span[@id="error_title"]')))
            if error_title.text == 'There was an error':
                return {"User Registered": False}
        except:
            # Check for password input
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
            if password_input:
                return {"User Registered": True}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = AWSLogin(email)
    print(registration_result)
