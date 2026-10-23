from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Creates and closes a Selenium Chrome WebDriver."""

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None

    def get_driver(self):
        if self.driver is not None:
            return self.driver

        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1365,900")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )

        try:
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.implicitly_wait(5)
            return self.driver
        except Exception as error:
            print(f"Could not start Chrome WebDriver: {error}")
            print("Check that Google Chrome is installed and internet is available.")
            return None

    def quit_driver(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
