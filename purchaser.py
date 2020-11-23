from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver


class Purchaser(ABC):
    def __init__(self, driver: WebDriver, **kwargs):
        self.driver = driver
        self.kwargs = kwargs

    @abstractmethod
    def run(self):
        pass
