import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from purchaser import Purchaser
from util import send_notification


class AmazonPurchaser(Purchaser):
    def __init__(
            self,
            driver: WebDriver,
            amazon_url: str,
            product_polling_seconds: float,
            username: str,
            password: str,
            **kwargs
    ):
        super().__init__(
            driver=driver,
            amazon_url=amazon_url,
            product_polling_seconds=product_polling_seconds,
            username=username,
            password=password,
            **kwargs
        )
        self.amazon_url = amazon_url
        self.driver = driver
        self.product_polling_seconds=product_polling_seconds
        self.username = username
        self.password = password

    def run(self):
        while not self._check_if_available():
            print("Item not available")
            time.sleep(self.product_polling_seconds)
            self.driver.refresh()
        send_notification('Item available for purchase!')

        self._find_by_id_and_click('add-to-cart-button')
        time.sleep(0.1)
        self._find_by_id_and_click('hlb-ptc-btn-native')

        self._login_if_required()

        time.sleep(0.25)
        self._wait_for_spinner_to_leave()

        delivery_options = self.driver.find_elements_by_class_name('a-radio-label')
        fastest_delivery_option = delivery_options[-1]
        fastest_delivery_option.click()

        self._wait_for_spinner_to_leave()

        place_order = WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(
                (By.CLASS_NAME, "place-your-order-button")
            )
        )
        place_order.click()
        time.sleep(2)

        try:
            self.driver.find_elements_by_class_name('a-color-success')
            send_notification("Purchase successful!")
        except NoSuchElementException:
            pass

    def _login_if_required(self):
        try:
            email_field = self.driver.find_element_by_id('ap_email')
            email_field.send_keys(self.username)
            self._find_by_id_and_click('continue')

            password_field = self.driver.find_element_by_id('ap_password')
            password_field.send_keys(self.password)
            self.driver.find_element_by_class_name('a-checkbox-label').click()
            self._find_by_id_and_click('signInSubmit')
        except NoSuchElementException:
            pass

    def _check_if_available(self):
        try:
            self.driver.get(self.amazon_url)
            self.driver.find_element_by_id('outOfStock')
        except NoSuchElementException:
            return True
        else:
            return False

    def _find_by_id_and_click(self, id: str) -> None:
        self.driver.find_element_by_id(id).click()

    def _wait_for_spinner_to_leave(self):
        while True:
            try:
                spinner = self.driver.find_element_by_id('spinner-anchor')
                if not spinner.is_displayed():
                    break
            except NoSuchElementException:
                break
