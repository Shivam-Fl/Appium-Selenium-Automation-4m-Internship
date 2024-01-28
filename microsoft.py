from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def MicrosoftRegister(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://signup.live.com/')

    try:
        wait = WebDriverWait(driver, 10)

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="MemberName"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on the signup button
        signup_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="iSignupAction"]')))
        signup_button.click()

        try:
            # Try to find a div with text "is already a Microsoft account. Please try a different email address."
            error_div = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "is already a Microsoft account. Please try a different email address.")]')))

            # If the error div is found, user registration failed
            if error_div:
                return {"User Registered": True}

        except:
            # Expect for a div with text "Create a password"
            create_password_div = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Create a password")]')))

            # If the create password div is found, user registration succeeded
            if create_password_div:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = MicrosoftRegister(email)
    print(registration_result)
