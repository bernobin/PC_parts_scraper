import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def fetch_categories_dynamic(base_url):
    options = Options()
    # Uncomment this line if you want to see the browser
    # options.add_argument("--headless")  # Comment out if you want to see the browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Opening the URL...")
        driver.get(base_url)

        # Wait for the page to load fully before interacting with any element
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Page loaded.")

        # Add a 10-second wait after the page is opened for observation
        print("Waiting for 10 seconds to observe...")
        time.sleep(10)  # Wait for 10 seconds to observe the initial page state

        # Click on the category panel to open it (assuming it's the element with the class 'f_phoneCatMenu')
        print("Waiting for the category panel to be clickable...")
        try:
            category_panel = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "f_phoneCatMenu"))
            )
            category_panel.click()  # Click the category panel to open it
            print("Clicked on the category panel to open.")
        except Exception as e:
            print("Timeout or error while clicking the category panel.")
            print(str(e))
            return []

        # Wait until the category menu is present (adjusted wait time)
        print("Waiting for category menu to load...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "categoryMenuItem_"))
            )
            print("Category menu loaded.")
        except Exception as e:
            print("Timeout or error while waiting for category menu.")
            print(str(e))
            return []

        # Attempt to find the menu and extract links
        try:
            menu = driver.find_element(By.ID, "categoryMenuItem_")
            links = menu.find_elements(By.TAG_NAME, "a")
            categories = []

            for link in links:
                href = link.get_attribute("href")
                if href and "/produktsuche/" in href:
                    categories.append(href)

            print(f"Found {len(categories)} main category links.")
        except Exception as e:
            print("Error while extracting category links.")
            print(str(e))
            categories = []

        # Stack to hold submenus for DFS
        submenu_stack = []

        # Find all submenus with class 'sub'
        print("Finding submenus...")
        submenus = driver.find_elements(By.CLASS_NAME, "sub")
        print(f"Found {len(submenus)} submenus.")

        for submenu in submenus:
            try:
                # Wait for submenu to be clickable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(submenu)
                )

                # Scroll to the submenu to ensure it's in view
                driver.execute_script("arguments[0].scrollIntoView(true);", submenu)

                # Click on the submenu
                submenu_id = submenu.get_attribute("data-id")
                print(f"Clicked on submenu {submenu_id}.")

                actions = ActionChains(driver)
                actions.move_to_element(submenu).click().perform()

                # Wait for the submenu's menu to load (ensure submenu content is visible)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, f"categoryMenuItem_{submenu_id}"))
                )

                # Locate the container using the ID
                submenu_container = driver.find_element(By.ID, f"categoryMenuItem_{submenu_id}")

                # Find all the links (anchor tags) inside the container
                links = submenu_container.find_elements(By.TAG_NAME, "a")

                # Extract href attributes from the links
                submenu_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

                # Print the links found
                print(f"Found {len(submenu_links)} links inside the submenu container {submenu_id}.")
                for link in submenu_links:
                    print(link)




                # Extract submenu links
                submenu_menu = driver.find_element(By.ID, f"categoryMenuItem_{submenu_id}")
                submenu_links = submenu_menu.find_elements(By.TAG_NAME, "a")
                for submenu_link in submenu_links:
                    href = submenu_link.get_attribute("href")
                    if href and "/produktsuche/" in href:
                        categories.append(href)

                # Find and click the back button to return to the parent menu
                back_button = driver.find_element(By.CLASS_NAME, "backToParent")
                if back_button:
                    back_button.click()
                    print(f"Navigated back using parent ID: {submenu_id}")
                    # Wait for the category menu to load again after going back
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "categoryMenuItem_"))
                    )

            except Exception as e:
                print(f"Error while processing submenu")
                print(f"Error details: {str(e)}")
                traceback.print_exc()  # Full stack trace for debugging

        return categories

    except Exception as e:
        print("Error occurred during execution:")
        print(f"Error details: {str(e)}")


if __name__ == "__main__":
    base_url = "https://www.toppreise.ch/"  # Replace with your actual base URL
    categories = fetch_categories_dynamic(base_url)
    print(f"Fetched categories:")
    for c in categories:
        print(c)