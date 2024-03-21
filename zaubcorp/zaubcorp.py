from flask import Flask, render_template, request, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time

app = Flask(__name__)

# Function to scrape data from a single page
# Function to scrape data from a single page
def scrape_page(driver):
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data = []
        rows = soup.find_all('tr', class_='odd') + soup.find_all('tr', class_='even')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 3:
                entry = {}
                entry['ID'] = cols[0].find('h5').text.strip()
                entry['Name'] = cols[1].find('h5').text.strip()
                entry['Company'] = cols[2].find('a').text.strip()
                data.append(entry)
        return data
    except Exception as e:
        print(f"Error in scraping: {str(e)}")
        return []



# Function to get total number of pages
def get_total_pages(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pagination_div = soup.find('div', id='results_paginate')
    if pagination_div:
        pages = pagination_div.find_all('li', class_='paginate_button')
        return len(pages) - 2
    else:
        return 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    name = request.json.get('name')  # Retrieve 'name' from JSON data

    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    try:
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

        if all_data:
            return jsonify(all_data)
        else:
            return jsonify({'error': 'No data found.'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        driver.quit()

@app.route('/download', methods=['POST'])
def download():
    data = json.loads(request.form['data'])
    if data:
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        excel_file_path = f'data_{timestamp}.xlsx'
        df.to_excel(excel_file_path, index=False)
        return send_file(excel_file_path, as_attachment=True)
    else:
        return jsonify({'error': 'No data provided for download.'})

if __name__ == "__main__":
    app.run(debug=True)
