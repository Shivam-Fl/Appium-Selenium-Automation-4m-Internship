from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def CodeChefRegister(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.codechef.com/signup')

    try:
        wait = WebDriverWait(driver, 10)

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="edit-mail"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on the username input (without entering anything)
        password_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
        password_input.click()

        try:
            # Try to find a div with text "Email already taken"
            error_div = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Email already taken")]')))

            # If the error div is found
            if error_div:
                return {"User Registered": True}

        except:
            # If the error div is not found
            return {"User Registered": False}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = CodeChefRegister(email)
    print(registration_result)
