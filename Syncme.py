import base64
import io
import time
from PIL import Image
from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def SyncMe(phone_number: str) -> Dict[str, str]:
    try:
        # Appium desired capabilities for Sync.ME app
        cap: Dict[str, Any] = {
            'platformName': 'Android',
            'deviceName': 'emulator-3554',
            "automationName": "uiautomator2",
            'language': 'en',
            'locale': 'US'
        }

        # Appium server URL
        url = 'http://localhost:4723/wd/hub'

        # Initialize Appium driver
        driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))

        # Set explicit wait timeout
        wait = WebDriverWait(driver, 20)

        # Find and click the Sync.ME app icon on the home screen
        syncme_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Sync.ME"]')))
        syncme_icon.click()

        # Find and click the History button
        history_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.syncme.syncmeapp:id/activity_main__tab__history')))
        history_button.click()

        # Find and click the search bar
        search_bar = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.syncme.syncmeapp:id/searchBarView')))
        search_bar.click()

        # Enter the phone number in the search bar
        phone_number_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.syncme.syncmeapp:id/phoneNumberEditText')))
        phone_number_field.send_keys(phone_number)

        # Click on the search button
        number_search_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.syncme.syncmeapp:id/searchFab')))
        number_search_button.click()

        # Click on the contact 
        contact_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.syncme.syncmeapp:id/titleTextView')))
        contact_element.click()

        # Extract the name from the name element
        name_element = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.syncme.syncmeapp:id/com_syncme_contact_details_actionbar_header__titleTextView')))
        contact_name = name_element.text

        # Find and extract the profile picture
        image_element = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.syncme.syncmeapp:id/avatarImageView')))
        screenshot = image_element.screenshot_as_png
        ss = Image.open(io.BytesIO(screenshot))
        imagebytes = io.BytesIO()
        ss.save(imagebytes, format='PNG')
        imagebytes.seek(0)
        enc_image = base64.b64encode(imagebytes.getvalue()).decode('utf-8')

        # Extract other details if available
        try:
            other_details_element = wait.until(
                EC.presence_of_all_elements_located((AppiumBy.ID, 'com.syncme.syncmeapp:id/subtitleTextView')))
            other_details = [element.text for element in other_details_element]
        except:
            other_details = []

        time.sleep(2)
        driver.terminate_app('com.syncme.syncmeapp')

        result = {"Name": contact_name, "profile_photo": enc_image}
        if other_details:
            result["Other_Details"] = other_details

        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}
    finally:
        driver.quit()

if __name__ == "__main__":
    # Get user input for the phone number
    phone_number = input("Enter the phone number: ")
    result = SyncMe(phone_number)
    print(result)
