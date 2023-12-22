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

def phonePe(user_input: str) -> Dict[str, str]:
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

        # Find and click the app icon
        el = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="PhonePe"]')
        el.click()

        # Set explicit wait timeout
        wait = WebDriverWait(driver, 15)

        # Find and click pay a mobile number option
        el1 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//androidx.recyclerview.widget.RecyclerView[@resource-id="com.phonepe.app:id/recycler_view"])[1]/android.view.ViewGroup[1]')))
        el1.click()

        # Find and click search bar
        el2 = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.LinearLayout[@resource-id="com.phonepe.app:id/toolbar_btn_container"]')))
        el2.click()

        # Find the EditText element
        el3 = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.phonepe.app:id/et_search_box"]')))
        el3.clear()
        # Set the user input as the new text in the EditText
        el3.send_keys(user_input)

        # Find the name obtained
        el4 = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.phonepe.app:id/tvNumberName"]')))
        name = el4.text

        #Find the profile picture and take a screenshot
        el5 = wait.until(EC.visibility_of_element_located(
            (AppiumBy.ID, 'com.phonepe.app:id/ivNumberImage')))
        screenshot = el5.screenshot_as_png
        ss = Image.open(io.BytesIO(screenshot))
        imagebytes = io.BytesIO()
        ss.save(imagebytes, format='PNG')
        imagebytes.seek(0)
        enc_image = base64.b64encode(imagebytes.getvalue()).decode('utf-8')
        time.sleep(2)
        driver.terminate_app('com.phonepe.app')

        # Extract name and return it
        return {"name": name, 'profile photo': enc_image}
       

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.terminate_app('com.phonepe.app')
        return {"error": str(e)}
    finally:
        driver.quit()
if __name__ == "__main__":
    # Get user input for the 10-digit number
    user_input = input("Enter a 10-digit number: ")

    if not user_input.isdigit() or len(user_input) != 10:
        print("Invalid input. Please enter a valid 10-digit number.")
    else:
        result = phonePe(user_input)
        print(result)
