from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
from datetime import datetime

# Function to scrape data from a single page
def scrape_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = []
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # Check if the row has the expected number of columns
        if len(cols) == 3:
            entry = {}
            entry['ID'] = cols[0].h5.text
            entry['Name'] = cols[1].h5.text
            entry['Company'] = cols[2].a.text
            data.append(entry)
    return data


# Function to get total number of pages
def get_total_pages(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pagination_div = soup.find('div', id='results_paginate')
    if pagination_div:
        pages = pagination_div.find_all('li', class_='paginate_button')
        return len(pages) - 2
    else:
        return 1

# Main function
def main():
    # Get user input
    name = input("Enter name: ")

    # Set up Selenium
    driver = webdriver.Chrome()
    base_url = "https://www.zaubacorp.com/directorsearchresults/"
    url = base_url + name
    driver.get(url)

    # Set entries to 100 if the select option is available
    try:
        select = Select(driver.find_element(By.NAME, 'results_length'))
        try:
            select.select_by_value('100')
        except:
            select.select_by_value('50')
    except:
        pass

    # Scraping data
    total_pages = get_total_pages(driver)
    all_data = []
    for page_num in range(total_pages):
        data = scrape_page(driver)
        all_data.extend(data)

        if page_num > 0:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(50, document.body.scrollHeight);")
            # Wait for a brief moment to ensure the button becomes clickable
            time.sleep(1)
            # Click the "Next" button
            next_page_link = driver.find_element(By.XPATH, "//a[text()='Next']")
            next_page_link.click()

    # Close the browser
    driver.quit()

    if not all_data:
        print("No data found.")
        return
    # Convert data to DataFrame
    if all_data:
        df = pd.DataFrame(all_data)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Specify the path to save the Excel file
        excel_file_path = f'{name}_{timestamp}.xlsx'

        # Save DataFrame to Excel
        df.to_excel(excel_file_path, index=False)

        print("Data scraped successfully and saved to Excel file:", excel_file_path)

if __name__ == "__main__":
    main()
