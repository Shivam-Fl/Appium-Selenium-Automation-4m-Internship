from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def eBayLogin(username):
    # Set up the WebDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.ebay.com/")

    try:
        # Declare the wait condition for elements to be clickable and present
        wait = WebDriverWait(driver, 10)

        # Find the Sign in link and click on it
        sign_in_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
        )
        sign_in_link.click()

        # Find the email input field and enter the username
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, 'userid'))
        )
        email_input.clear()
        email_input.send_keys(username)

        # Click on the Continue button
        continue_button = wait.until(
            EC.element_to_be_clickable((By.ID, 'signin-continue-btn'))
        )
        continue_button.click()

        # Find the error message if any
        try:
            error_message = wait.until(
                EC.visibility_of_element_located((By.ID, 'errormsg'))
            )
            if error_message:
                return {"User Registered": False}
        except:
            # Find the welcome message
            welcome_message = wait.until(
                EC.visibility_of_element_located((By.ID, 'welcome-msg'))
            )
            if welcome_message:
                return {"User Registered": True}

    except Exception as e:
        print("Exception occurred:", e)

    finally:
        # Close the browser window
        driver.quit()

if __name__ == "__main__":

    username = input("Enter your eBay username: ")
    result = eBayLogin(username)
    print(result)
