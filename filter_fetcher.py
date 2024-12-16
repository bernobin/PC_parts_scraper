from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the webpage
    url = "https://www.toppreise.ch/produktsuche/Computer-Zubehoer/PC-Komponenten/Grafikkarten-Zubehoer/Grafikkarten-c37?sfh=oi%7Eongff417x14%3Asv104433%2Bs%7Epa"
    driver.get(url)

    # Wait for JavaScript content to load (use explicit waits for better control)
    driver.implicitly_wait(10)

    # Find filter checkboxes (adjust XPath or CSS selectors based on the site structure)
    filter_elements = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

    # Extract filter data
    filters = []
    for filter_elem in filter_elements:
        name = filter_elem.get_attribute("name")
        filter_id = filter_elem.get_attribute("id")
        if name or filter_id:
            filters.append({"name": name, "id": filter_id})

    # Print the results
    for filter_info in filters:
        print(f"Filter Name: {filter_info['name']}, Filter ID: {filter_info['id']}")

finally:
    # Close the browser
    driver.quit()
