from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

class TestSmoke:

    def setup_method(self, method):
        opts = Options()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)
        self.driver.implicitly_wait(5)

    def teardown_method(self, method):
        self.driver.quit()

    def test_smoke(self):
        driver = self.driver

        # Open site
        driver.get("http://127.0.0.1:5500/cse270/teton/1.6/index.html")

        # --- Test 1: Logo/Header ---
        assert "Teton Idaho CoC" in driver.title
        assert driver.find_element(By.TAG_NAME, "h1").text == "Teton Idaho Chamber of Commerce"

        # --- Test 2: Home Page ---
        assert driver.find_element(By.LINK_TEXT, "Join Us")

        # --- Test 3: Directory Page ---
        driver.get("http://127.0.0.1:5500/cse270/teton/1.6/directory.html")
        assert "Teton Turf and Tree" in driver.page_source

        # --- Test 4: Join Page ---
        driver.get("http://127.0.0.1:5500/cse270/teton/1.6/join.html")
        driver.execute_script("document.getElementsByName('fname')[0].value='John';")
        driver.execute_script("document.getElementsByName('lname')[0].value='Doe';")
        driver.execute_script("document.getElementsByName('phone')[0].value='208-555-1234';")

        # --- Test 5: Admin Page ---
        driver.get("http://127.0.0.1:5500/cse270/teton/1.6/admin.html")
        driver.execute_script("document.getElementsByName('username')[0].value='wrong';")
        driver.execute_script("document.getElementsByName('password')[0].value='wrong';")

        driver.find_element(By.TAG_NAME, "button").click()

        assert "Invalid" in driver.page_source