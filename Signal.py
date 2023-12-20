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

def Signal(phone_number: str) -> Dict[str, str]:
    try:
        # Appium desired capabilities
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

        # Find and click the Signal app icon on the home screen
        signal_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Signal"]')))
        signal_icon.click()

        # Find and click the pencil icon for a new chat
        pencil_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="New chat"]')))
        pencil_icon.click()

        # Find and click the search bar
        search_bar = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="org.thoughtcrime.securesms:id/search_view"]')))
        search_bar.click()

        # Enter the phone number in the search bar
        search_bar.send_keys(phone_number)

        # Find and click on the contact with the entered phone number
        contact_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="org.thoughtcrime.securesms:id/name"]')))
        contact_element.click()

        
        try:
            # Check if user is registered or not
            not_found_element = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/message"]')))
            if not_found_element:
                return {"Message": phone_number + ' is not a Signal user'}

            
        except:
            # Check if the image element is present
            image_element = wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="org.thoughtcrime.securesms:id/contact_photo_container"]')))
            # Find and extract the profile picture
            screenshot = image_element.screenshot_as_png
            ss = Image.open(io.BytesIO(screenshot))
            imagebytes = io.BytesIO()
            ss.save(imagebytes, format='PNG')
            imagebytes.seek(0)
            enc_image = base64.b64encode(imagebytes.getvalue()).decode('utf-8')
            time.sleep(2)

            return {"Message": phone_number + ' is registered on Signal app', "profile_photo": enc_image}

        

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}
    finally:
        driver.quit()

if __name__ == "__main__":
    # Get user input for the phone number
    phone_number = input("Enter the phone number: ")
    result = Signal(phone_number)
    print(result)
