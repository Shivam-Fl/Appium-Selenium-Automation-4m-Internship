import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def automate_notion(email, user_profile="C:/Users/a2z/AppData/Local/Google/Chrome/User Data/Default"):
    # Set Chrome options
    chrome_options = Options()
    # Add user data directory to Chrome options
    chrome_options.add_argument("user-data-dir=" + user_profile)
    # Maximize the browser window
    chrome_options.add_argument("--start-maximized")

    # Initialize ChromeDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.notion.so")

    try:
        # Find and click on "Settings & members"
        settings_members = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Settings & members']")))
        settings_members.click()

        # Wait for the "Add members" button to be clickable
        add_members_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Add members']")))

        # Click on "Add members" button
        add_members_button.click()

        # Find and input email
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search name or emails']")))
        email_input.send_keys(email)

        # Find and press Enter to confirm the email
        email_input.send_keys(Keys.ENTER)

        time.sleep(5)

        # Find the parent div which have  name element within it

        parent_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                       "//div[@style='margin-left: 6px; margin-right: 12px; min-width: 0px; flex: 1 1 auto;']")))

        # Extract text from the parent div
        text_content = parent_div.text.strip()
        if text_content == email:
            print("Username not found")
        else:
            print("Username: " + text_content)

    finally:
        # Close the browser
        driver.quit()


email = input("Enter email: ")
automate_notion(email)
