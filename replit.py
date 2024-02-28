from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ReplitSignup(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://replit.com/signup')

    try:
        # Click on "Continue with email"
        continue_with_email = driver.find_element(By.XPATH, '//a[contains(text(), "Continue with email →")]')
        continue_with_email.click()

        # Enter email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Try to find "Email already in use" text
        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Email already in use")]')))
            if error_message:
                return {"User Registered": True}
        except:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = ReplitSignup(email)
    print(registration_result)
