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
import threading

# Set up Chrome WebDriver in headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-features=NetworkService')
options.add_argument('--window-size=1920x1080')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')

# Install ChromeDriver if not already installed
service = Service(ChromeDriverManager().install())

# URL of the website
url = 'https://hprera.nic.in/PublicDashboard'

projects = []
lock = threading.Lock()

def process_link(link_text, tab_index):
    local_driver = webdriver.Chrome(service=service, options=options)
    try:
        # Open the main page in the new driver instance
        local_driver.get(url)
        WebDriverWait(local_driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        time.sleep(30)  # Wait for the page to load completely
        
        link = WebDriverWait(local_driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text.strip()))
        )
        link.click()
        
        # Wait for the modal or dynamic content to load
        time.sleep(10)
        
        # Get the updated page source
        new_page_source = local_driver.page_source
        new_soup = BeautifulSoup(new_page_source, 'html.parser')
        
        # Extract the relevant information
        project_info = {}
        table_rows = new_soup.find_all('tr')
        for row in table_rows:
            columns = row.find_all('td')
            if len(columns) >= 2:
                key = columns[0].text.strip()
                value = columns[1].text.strip() if columns[1].text.strip() != 'N/A' else None
                if key in ["Name", "PAN No.", "GSTIN No.", "Permanent Address"]:
                    project_info[key] = value
        
        json_project_info = json.dumps(project_info, ensure_ascii=False)
        
        with lock:
            projects.append({link_text.strip(): json_project_info})
        
    except Exception as e:
        print(f"Error processing link {link_text}: {e}")
    finally:
        local_driver.quit()

# Main script
try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    time.sleep(30)  # Wait for the page to load completely
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    reras = soup.find_all('a', title='View Application', limit=5)
    
    threads = []
    for i, rera in enumerate(reras):
        link_text = rera.text.strip()
        thread = threading.Thread(target=process_link, args=(link_text, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
finally:
    driver.quit()

# Print the extracted project information
for project in projects:
    print(project)
