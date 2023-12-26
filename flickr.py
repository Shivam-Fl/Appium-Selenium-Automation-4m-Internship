import base64
import io
from PIL import Image
from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def FlickrProfile(email: str) -> Dict[str, str]:
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
        wait = WebDriverWait(driver, 15)

        # Find and click the Flickr app icon on the home screen
        flickr_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Flickr"]')))
        flickr_icon.click()

        # Find and click the search button
        search_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Search"]')))
        search_button.click()

        # Find and click the search bar
        search_bar = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.flickr.android:id/search_view_autocompl_textview')))
        search_bar.click()
        driver.implicitly_wait(10)
        
        # Enter the email in the search bar
        search_bar1 = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.flickr.android:id/search_view_autocompl_textview"]')
        search_bar1.send_keys(email)

        # Press Enter
        driver.press_keycode(66)  # KeyEvent.KEYCODE_ENTER

        # Wait for the People tab to be clickable
        people_tab = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.flickr.android:id/sliding_tab_title" and @text="People"]')))
        people_tab.click()

        # Click on the People icon
        try:
            people_icon = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.flickr.android:id/people_list_item_icon"]')))
            people_icon.click()

            # Go to About
            about_tab = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.flickr.android:id/sliding_tab_title" and @text="About"]')))
            about_tab.click()

        # Find and extract the profile image (unchanged)
            profile_image_element = wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.flickr.android:id/profile_avatar_bar_iv"]')))
            screenshot = profile_image_element.screenshot_as_png
            ss = Image.open(io.BytesIO(screenshot))
            imagebytes = io.BytesIO()
            ss.save(imagebytes, format='PNG')
            imagebytes.seek(0)
            enc_image = base64.b64encode(imagebytes.getvalue()).decode('utf-8')

        # Extract label and content
            try:
            # Wait for label and content elements with XPATH
                label_elements = wait.until(
                  EC.visibility_of_all_elements_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.flickr.android:id/profile_bio_label"]')))
                content_elements = wait.until(
                EC.visibility_of_all_elements_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.flickr.android:id/profile_bio_content"]')))

                labels = []
                contents = []

            # Skip the first label
                photo_element = label_elements[0]
                label_elements = label_elements[1:]
                photo_count = photo_element.text

                for (label_element, content_element) in zip(label_elements, content_elements):
                    label = label_element.text
                    content = content_element.text

                    labels.append(label)
                    contents.append(content)

            # Merge labels and contents into key-value pairs
                labels_and_contents = [{"label": label, "content": content} for label, content in zip(labels, contents)]

                result = {"Additional Data": labels_and_contents, "profile_image": enc_image, "photo count": photo_count}
                driver.terminate_app('com.flickr.android')
                driver.quit()
                return result
            except Exception as e:
                result = {"profile_image": enc_image}
                driver.terminate_app('com.flickr.android')
                driver.quit()
                return result
        
        except Exception as pe:
            
            driver.terminate_app('com.flickr.android')  # Terminate the app
            driver.quit()  # Quit the driver
            return {"error": "User not found"}

        

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.terminate_app('com.flickr.android')
        driver.quit()
        return {"error": str(e)}
  

if __name__ == "__main__":
    # Get user input for the email
    email = input("Enter the email: ")
    result = FlickrProfile(email)
    print(result)
