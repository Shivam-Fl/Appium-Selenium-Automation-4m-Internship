from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def HackerRankRegister(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.hackerrank.com/auth/signup')

    try:
        wait = WebDriverWait(driver, 10)

        # Find and insert email
        email_input = wait.until(EC.presence_of_element_located((By.ID, 'input-2')))
        email_input.clear()
        email_input.send_keys(email)

        # Wait for 2 seconds
        time.sleep(5)

        try:
            # Try to find a div with class "d-flex align-items-start error-message" and text "Already registered."
            error_div = wait.until(
                EC.visibility_of_element_located((By.XPATH,
                                                  '//div[@class="d-flex align-items-start error-message" and contains(text(), "Already registered.")]')))

            # If the error div is found, user registration failed
            if error_div:
                return {"User Registered": True}



        except:
            return {"User Registered": False}

    except Exception as e:
        print("Error:", e)


    finally:
        driver.quit()


if __name__ == "__main__":
    email = input("Enter your email: ")
    registration_result = HackerRankRegister(email)
    print(registration_result)
