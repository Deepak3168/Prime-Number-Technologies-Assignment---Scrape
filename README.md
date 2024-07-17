### RERA Website Data Scraping

This documentation provides instructions on how to set up and run a Python script to scrape data from the Himachal Pradesh  RERA (Real Estate Regulatory Authority) website using Selenium and BeautifulSoup.

#### Prerequisites

Before running the script, ensure you have the following prerequisites installed:

1. **Python Environment**
   - Python 3.x installed on your system.

2. **Required Python Packages**
   - After cloning the repository, navigate to the project directory and install the required packages using:
     ```bash
     pip install -r requirements.txt
     ```
   - This command installs necessary packages including Selenium, BeautifulSoup, and others specified in `requirements.txt`.

3. **Google Chrome Browser and WebDriver**
   - Ensure Google Chrome browser is installed on your machine.
   - Install ChromeDriver for Selenium. The script uses `webdriver_manager.chrome.ChromeDriverManager` to manage ChromeDriver automatically, but ensure it's installed locally.

#### Running the Script

1. **Clone the Repository**
   - Clone the repository containing the script:
     ```bash
     git clone https://github.com/Deepak3168/Scrape.git
     cd Scrape
     ```

3. **Execute the Script**
   - Run the script using Python:
     ```bash
     python scrape.py
     ```
   - This will execute the script, which will launch a headless Chrome browser, navigate to the specified URL, scrape the required data, and print the extracted project information.

### Note

- **Page Load Delays:** The script includes explicit `time.sleep()` commands to ensure sufficient time for page and content loading. Adjust these times based on your network speed and website responsiveness. For loading dynamic websites, these time intervals are set in the code, which may result in slower execution depending on the website's responsiveness.