from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def snapchatLogin(email):
    # Set up the WebDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get("https://accounts.snapchat.com/accounts/v2/login")

    try:
        # Declare the wait condition for elements to be present
        wait = WebDriverWait(driver, 10)

        # Find the email input field and enter the username
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, 'accountIdentifier'))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Click on the Next button
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        next_button.click()

        # Find and print the error message if any
        try:
            error_message = wait.until(
                EC.visibility_of_element_located((By.ID, 'error_message'))
            )
            if error_message:
                return {"User Registered": False}
        except:
            # Find and print the welcome message
            password_field = wait.until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            if password_field:
                return {"User Registered": True}

    except Exception as e:
        print("Exception occurred:", e)

    finally:
        # Close the browser window
        driver.quit()

if __name__ == "__main__":
    # Perform Snapchat login with username
    email = input("Enter your Snapchat email: ")
    result = snapchatLogin(email)
    print(result)
