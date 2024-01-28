from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def CodeforcesPasswordRecovery(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://codeforces.com/passwordRecovery')

    try:
        wait = WebDriverWait(driver, 10)


        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="handleOrEmail"]')))
        email_input.clear()
        email_input.send_keys(email)

        # Click on the "Recover" input
        recover_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Recover"]')))
        recover_input.click()

        try:
            # Try to find a span with class "error for__handleOrEmail" and specific text
            error_span = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//span[@class="error for__handleOrEmail" and contains(text(), "No such handle or email")]')))

            # If the error span is found, user registration failed
            
            if error_span:
                return {"User Registered": False}

        except:
            # Expect for a div with specific text
            success_div = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="centered-message" and contains(text(), "Password recovery letter has been sent successfully")]')))

            # If the success div is found, user registration succeeded
            if success_div:
                return {"User Registered": True}

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter your email: ")
    recovery_result = CodeforcesPasswordRecovery(email)
    print(recovery_result)
