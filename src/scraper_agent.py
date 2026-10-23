import logging
import time
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from .driver_manager import DriverManager
from .data_models import Product
from .utils import save_data_to_json, wait_for_element

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ScraperAgent:
    """Scrapes products according to selectors in a JSON configuration."""

    def __init__(self, config, headless=True):
        self.config = config
        self.driver_manager = DriverManager(headless=headless)
        self.driver = None
        self.scraped_products = []
        self.max_pages = int(config.get("max_pages", 3))
        self.delay = float(config.get("delay_between_pages", 1))

    def _text(self, parent, selector):
        if not selector:
            return None
        try:
            value = parent.find_element(By.CSS_SELECTOR, selector).text.strip()
            return value or None
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def _attribute(self, parent, selector, attribute):
        if not selector:
            return None
        try:
            value = parent.find_element(By.CSS_SELECTOR, selector).get_attribute(attribute)
            return urljoin(self.driver.current_url, value) if value else None
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def scrape_current_page(self):
        selector = self.config["item_container_selector"]
        items = self.driver.find_elements(By.CSS_SELECTOR, selector)
        logging.info("Found %s product items.", len(items))

        for item in items:
            name = self._text(item, self.config["item_data_selectors"].get("name"))
            price = self._text(item, self.config["item_data_selectors"].get("price"))
            if not name or not price:
                continue

            product = Product(
                name=name,
                price=price,
                description=self._text(item, self.config["item_data_selectors"].get("description")),
                url=self._attribute(item, self.config["item_data_selectors"].get("url"), "href"),
                image_url=self._attribute(item, self.config["item_data_selectors"].get("image_url"), "src"),
            )
            self.scraped_products.append(product.to_dict())

    def run(self):
        self.driver = self.driver_manager.get_driver()
        if self.driver is None:
            return []

        try:
            self.driver.get(self.config["start_url"])
            for page_number in range(1, self.max_pages + 1):
                logging.info("Scraping page %s: %s", page_number, self.driver.current_url)
                wait_for_element(
                    self.driver,
                    By.CSS_SELECTOR,
                    self.config["item_container_selector"],
                    timeout=10,
                )
                self.scrape_current_page()

                next_selector = self.config.get("pagination_selector")
                if not next_selector or page_number == self.max_pages:
                    break

                next_links = self.driver.find_elements(By.CSS_SELECTOR, next_selector)
                if not next_links:
                    logging.info("No next page found. Stopping.")
                    break

                next_url = next_links[0].get_attribute("href")
                if not next_url:
                    logging.info("Next page link has no URL. Stopping.")
                    break

                self.driver.get(urljoin(self.driver.current_url, next_url))
                time.sleep(self.delay)
        except Exception as error:
            logging.exception("Scraping stopped because of an error: %s", error)
        finally:
            self.driver_manager.quit_driver()

        output_path = save_data_to_json(
            self.scraped_products,
            self.config.get("output_filename", "scraped_products.json"),
            self.config.get("output_directory", "data"),
        )
        logging.info("Scraping finished. Total products scraped: %s", len(self.scraped_products))
        logging.info("Output file: %s", output_path)
        return self.scraped_products
