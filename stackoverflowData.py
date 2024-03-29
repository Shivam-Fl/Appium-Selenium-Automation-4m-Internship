from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json



# Function to extract user information
def extract_user_info(user_div, driver):
    try:
        # Extracting user ID and name from the user-details div
        user_details_div = user_div.find('div', class_='user-details')
        user_id_link = user_details_div.find('a')['href'] if user_details_div.find('a') else "N/A"
        user_id = user_id_link.split('/')[-2] if user_id_link != "N/A" else "N/A"
        user_name = user_details_div.find('a').text.strip() if user_details_div.find('a') else "N/A"
    except Exception as e:
        print("Error extracting user ID and name:", e)
        user_id = "N/A"
        user_name = "N/A"

    try:
        user_location = user_div.find('span', class_='user-location').text.strip()
    except Exception as e:
        print("Error extracting user location:", e)
        user_location = "N/A"

    try:
        reputation_score = user_div.find('span', class_='reputation-score').text.strip()
    except Exception as e:
        print("Error extracting reputation score:", e)
        reputation_score = "N/A"

    try:
        user_tags = [tag.text.strip() for tag in user_div.select(".user-tags a")]
    except Exception as e:
        print("Error extracting user tags:", e)
        user_tags = []

    # Extract user image
    user_image = extract_user_image(user_div)

    return {
        'id': user_id,
        'name': user_name,
        'location': user_location,
        'reputation': reputation_score,
        'tags': user_tags,
        'image': user_image
    }



# Function to extract image or Gravatar link
def extract_user_image(user_div):
    try:
        gravatar_url = user_div.select_one("img")["src"]
        return gravatar_url
    except Exception as e:
        print("Error extracting user image:", e)
        return "N/A"


# Function to automate the process on Stack Overflow
def stack_overflowData(name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(f"https://stackoverflow.com/users?page=1&tab=reputation&filter=week&search={name}")

    users_info = []

    # Extract user information from the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    user_divs = soup.find_all('div', class_='grid--item')
    if 'user-hover' not in user_divs[0]['class']:  # Check if single entry
        user_info = extract_user_info(user_divs[0], driver)
        users_info.append(user_info)
    else:  # Multiple entries
        for user_div in user_divs:
            if 'user-info' in user_div['class']:
                user_info = extract_user_info(user_div, driver)
                users_info.append(user_info)

    # Check for pagination
    pagination_div = soup.find('div', class_='s-pagination')
    if pagination_div:
        while True:
            next_page_link = pagination_div.find('a', rel='next')
            if next_page_link:
                next_page_url = next_page_link['href']
                print("Next page URL:", next_page_url)
                driver.get("https://stackoverflow.com" + next_page_url)
                # Wait for page to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='user-browser']")))

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                user_divs = soup.find_all('div', class_='grid--item')
                for user_div in user_divs:
                    if 'user-info' in user_div['class']:
                        user_info = extract_user_info(user_div, driver)
                        users_info.append(user_info)

                pagination_div = soup.find('div', class_='s-pagination')
            else:
                break

    driver.quit()

    return users_info


# Main function
def main():
    name = input("Enter name: ")
    extracted_data = stack_overflowData(name)
    print(json.dumps(extracted_data))


if __name__ == "__main__":
    main()
