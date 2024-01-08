from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def FlickrProfileInfo(email):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.flickr.com/')

    try:
        wait = WebDriverWait(driver, 10)

        # Click on the search field and enter email
        search_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="search-field"]')))
        search_field.click()
        search_field.send_keys(email)
        search_field.send_keys(u'\ue007')  # Press Enter

        # Click on "People" div
        people_div = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="People"]')))
        people_div.click()



        try:
            # Click on the first anchor tag with class "click anywhere" and data-track
            group_card_other_click = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[@class="click-anywhere" and @data-track="groupCardOtherClick"]')))
            group_card_other_click.click()

            # Click on "About" span
            about_span = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="About"]')))
            about_span.click()

            # Extract profile image URL
            avatar_container = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="avatar-container"]')))
            profile_image_url = avatar_container.find_element(By.XPATH, './/div[contains(@style, "background-image")]').get_attribute('style')
            profile_image_url = profile_image_url.split('url("', 1)[1].split('")')[0]

            # Extract name
            title_container = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="title-container"]')))
            name = title_container.find_element(By.XPATH, './/h1').text

            # Extract subtitle
            subtitle = wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="subtitle truncate"]')))
            subtitle_text = subtitle.text

            # Extract description
            description_container = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="description-container"]')))
            description_text = description_container.find_element(By.XPATH, './/div[@class="description expanded"]/p').text

            # Extract joined date and link
            archives_link = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="archives-link"]')))
            joined_date = archives_link.text
            joined_link = archives_link.get_attribute('href')

            # Return the key-value object
            return {
                "User Registered": True,
                "Profile Image": profile_image_url,
                "Name": name,
                "Subtitle": subtitle_text,
                "Description": description_text,
                "Joined Date": {"text": joined_date, "link": joined_link}
            }

        except:
            no_result = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="no-results-message"]')))
            if no_result:
                return {"User Registered": False}

    except Exception as e:
        print("Error:", e)


    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Enter a Flickr email: ")
    profile_info = FlickrProfileInfo(email)
    print(profile_info)
