from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-features=NetworkService')
options.add_argument('--window-size=1920x1080')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')


service = Service(ChromeDriverManager().install())

url = 'https://hprera.nic.in/PublicDashboard'

projects = []

try:
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    print("Getting Data of rera Links.....")

    time.sleep(30)  

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    reras = soup.find_all('a', title='View Application', limit=5)
    
    
    for i, rera in enumerate(reras):
        try:
           
            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, rera.text.strip()))
            )
            link.click()
            
            print(f"Clicked Rera {i+1}")
            time.sleep(10)
            
            
            details_page= driver.page_source
            new_soup = BeautifulSoup(details_page, 'html.parser')
            
          
            project_info = {}
            table_rows = new_soup.find_all('tr')
            for row in table_rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    key = columns[0].text.strip()
                    value = columns[1].find('span').text.strip() if columns[1].find('span') else None
                    if key in ["Name", "PAN No.", "GSTIN No.", "Permanent Address"]:
                        project_info[key] = value
            
            project = json.dumps(project_info, ensure_ascii=False)
            projects.append({rera.text.strip(): project})
            
           
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Close")]'))
            )
            close_button.click()
            print(f"Closed {i+1}")  
            
        except Exception as e:
            print(f"Error processing link {i+1}: {e}")
            continue

finally:

    driver.quit()


for project in projects:
    for key, value in project.items():
        project_data = json.loads(value)
        print(f"RERA Number: {key}")
        print("Project Information:")
        for k, v in project_data.items():
            print(f"- {k}: {v}")
        print()
