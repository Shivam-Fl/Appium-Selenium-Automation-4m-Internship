from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def HackerEarthLogin(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.hackerearth.com/login/')

    try:
        wait = WebDriverWait(driver, 10)

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_login"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Generate a random password (you may use your password generation function here)
        password = "YourRandomPassword"

        # Enter password
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_password"]')))
        password_input.clear()
        password_input.send_keys(password)

        # Click on the Log In input
        login_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log In"]')))
        login_input.click()

        try:
            # Try to find an li with text "Please enter a valid emailid/username"
            error_li = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//li[contains(text(), "Please enter a valid emailid/username")]')))

            # If the error li is found, user registration failed
            if error_li:
                return {"User Registered": False}

        except:
            # Expect for an li with specific text
            error_li = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//li[contains(text(), "Wrong e-mail and/or password.")]')))

            # If the error li is found, user registration succeeded
            if error_li:
                return {"User Registered": True}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter your email: ")
    login_result = HackerEarthLogin(email)
    print(login_result)
