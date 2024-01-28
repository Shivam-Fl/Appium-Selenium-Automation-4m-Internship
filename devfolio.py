from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def DevfolioLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://devfolio.co/discover?auth=signin')

    try:
        wait = WebDriverWait(driver, 10)

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter your email or username"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on the Continue div
        continue_div = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Continue")]')))
        continue_div.click()

        try:
            # Try to find an input with id "password"
            password_input = wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))

            # If the password input is found, user registration succeeded
            if password_input:
                return {"User Registered": True}

        except:
            # Expect for a p with specific text
            error_p = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//p[contains(text(), "Sorry, we couldn\'t find an account with that email address.")]')))

            # If the error p is found, user registration failed
            if error_p:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    login_result = DevfolioLogin(email)
    print(login_result)
