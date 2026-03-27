from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        driver.get("http://127.0.0.1:5500/cse270-v16/cse270/teton/1.6/index.html")

        # --- Test 1: Logo/Header ---
        assert "Teton Idaho CoC" in driver.title
        assert driver.find_element(By.TAG_NAME, "h1").text == "Teton Idaho"

        # --- Test 2: Home Page ---
        assert driver.find_element(By.LINK_TEXT, "Join Us")

        # --- Test 3: Directory Page ---
        driver.get("http://127.0.0.1:5500/cse270-v16/cse270/teton/1.6/directory.html")
        WebDriverWait(driver, 10).until(
            lambda d: "Teton Turf and Tree" in d.page_source
        )
        assert "Teton Turf and Tree" in driver.page_source
    

        # --- Test 4: Join Page ---
        driver.get("http://127.0.0.1:5500/cse270-v16/cse270/teton/1.6/join.html")
        driver.execute_script("document.getElementsByName('fname')[0].value='John';")
        driver.execute_script("document.getElementsByName('lname')[0].value='Doe';")
        driver.execute_script("document.getElementsByName('bizname')[0].value='My Business';")
        driver.execute_script("document.getElementsByName('biztitle')[0].value='Boss';")
        driver.find_element(By.TAG_NAME, "input").click()
        assert "email" in driver.page_source.lower()
        # --- Test 5: Admin Page ---
        driver.get("http://127.0.0.1:5500/cse270-v16/cse270/teton/1.6/admin.html")
        driver.execute_script("document.getElementsByName('username')[0].value='wrong';")
        driver.execute_script("document.getElementsByName('password')[0].value='wrong';")

        driver.find_element(By.TAG_NAME, "input").click()

        assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()