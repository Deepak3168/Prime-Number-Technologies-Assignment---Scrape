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


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = 'https://hprera.nic.in/PublicDashboard'

projects = []

try:
    driver.get(url)
    print("Getting Data .....")
    time.sleep(30) 
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    reras = soup.find_all('a', title='View Application', limit=5)
    print(reras)
    
    for i, rera in enumerate(reras):
        try:
            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, rera.text.strip()))
            )
            link.click()
            time.sleep(10)
            new_page_source = driver.page_source
            new_soup = BeautifulSoup(new_page_source, 'html.parser')
            
            project_info = {}
            table_rows = new_soup.find_all('tr')
            for row in table_rows:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    key = columns[0].text.strip()
                    value = columns[1].text.strip() if columns[1].text.strip() != 'N/A' else None
                    if key in ["Name", "PAN No.", "GSTIN No", "Permanent Address"]:
                        project_info[key] = value
            
            json_project_info = json.dumps(project_info, ensure_ascii=False)
            
            projects.append({rera.text.strip(): json_project_info})
            
            
            driver.get(url)
            time.sleep(30)  
            
        except Exception as e:
            print(f"Error processing link {i+1}: {e}")
            continue

finally:
    driver.quit()

for project in projects:
    print(project)
