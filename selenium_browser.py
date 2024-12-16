import time
import json

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.toppreise.ch/"

# implement status?
# handle consent window


class SeleniumBrowser:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        print(f"opening {URL}")
        self.driver.get(URL)
        try:
            welcome = self.driver.find_element(By.CLASS_NAME, "fc-dialog-container")
            decline = welcome.find_element(By.CLASS_NAME, "fc-cta-do-not-consent")
            decline.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def click_category_menu(self) -> None:
        category_panel = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "f_phoneCatMenu"))
        )
        category_panel.click()
        print("Clicked on the category panel to open.")

    def category_is_active(self, data_id) -> bool:
        if data_id == '':
            print(f"cannot determine if menu {data_id} is active")
            return False
        ul_element = self.driver.find_element(By.ID, f"categoryMenuItem_{data_id}")
        classes = ul_element.get_attribute("class").split()
        return "f_CategoryMenuItemActive" in classes

    def category_menu_is_visible(self) -> bool:
        body_element = self.driver.find_element(By.TAG_NAME, "body")
        classes = body_element.get_attribute("class").split()
        return "showCategoryMenu" in classes

    def active_category_data_id(self) -> str:
        elements = self.driver.find_elements(By.CLASS_NAME, "categoryMenuItem")
        for element in elements:
            element_id = element.get_attribute("id")
            data_id = element_id.split('_')[1]
            if data_id != '' and self.category_is_active(data_id):
                return data_id
        return ''

    def visible_menus(self):
        if not self.category_menu_is_visible():
            return []

        data_id = self.active_category_data_id()
        ul_element = self.driver.find_element(By.ID, f"categoryMenuItem_{data_id}")
        a_elements = ul_element.find_elements(By.TAG_NAME, "a")
        submenus = [a.get_attribute("href") for a in a_elements if a.get_attribute("href")]

        return submenus

    def visible_submenus(self):
        if not self.category_menu_is_visible():
            return []

        data_id = self.active_category_data_id()
        ul_element = self.driver.find_element(By.ID, f"categoryMenuItem_{data_id}")
        a_elements = ul_element.find_elements(By.CLASS_NAME, "sub")
        hrefs = [a.get_attribute("data-id") for a in a_elements if a.get_attribute("data-id")]

        return hrefs

    def open_submenu(self, data_id):
        if data_id in self.visible_submenus():
            element = self.driver.find_element(By.CSS_SELECTOR, f'a[data-id="{data_id}"]')
            time.sleep(0.2)
            element.click()
            print(f"Clicked on the menu {data_id} to open.")

    def close_submenu(self, data_id):
        if data_id == self.active_category_data_id():
            ul_element = self.driver.find_element(By.ID, f"categoryMenuItem_{data_id}")
            time.sleep(0.2)
            back = ul_element.find_element(By.CLASS_NAME, "backToParent")
            back.click()
            print(f"Clicked on the menu {data_id} to close.")

    def explore(self, data_id='', menu=None):
        if data_id == '':
            self.click_category_menu()
            menu = []

        for data_id in self.visible_submenus():
            self.open_submenu(data_id)
            menu = self.explore(data_id, menu)
            self.close_submenu(data_id)

        return menu + self.visible_menus()


def main():
    try:
        browser = SeleniumBrowser(headless=False)
        menu = browser.explore()
        with open('./menu.json', 'w') as fo:
            json.dump(menu, fo)
    except selenium.common.exceptions.ElementClickInterceptedException:
        answer = input('unexpected hold-up, would you like to continue?')
        if answer:
            pass


if __name__ == '__main__':
    main()
