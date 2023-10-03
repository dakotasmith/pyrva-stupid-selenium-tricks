from abc import ABC, abstractmethod

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(ABC):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self._validate_page()

    def _validate_page(self):
        try:
            self.validate_page()
        except NoSuchElementException as exc:
            raise PageError(
                f'expected elements not found. {self.__class__.__name__} not loaded'
            ) from exc
        except AssertionError as exc:
            raise PageError(
                f'wait_for assert failed. {self.__class__.__name__} not loaded'
            ) from exc

    @abstractmethod
    def validate_page(self):
        pass

    def find_element(self, locator):
        element = None
        if isinstance(locator, tuple):
            element = self.driver.find_element(*locator)
        else:
            element = self.driver.find_element(locator)
        return element

    def find_elements(self, locator):
        elements = None
        if isinstance(locator, tuple):
            elements = self.driver.find_elements(*locator)
        else:
            elements = self.driver.find_elements(locator)
        return elements

    def wait_for_visibility(self, locator):
        try:
            self.wait.until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            raise ExpectedElementError(
                f'timeout waiting for visible element - locator {locator}'
            ) from None
        return

    def wait_for_invisibility(self, locator):
        try:
            self.wait.until(ec.invisibility_of_element_located(locator))
        except TimeoutException:
            raise ExpectedElementError(
                f'timeout waiting for invisible element - locator {locator}'
            ) from None
        return


class PageError(Exception):
    """Raise this error to fail a page in an unknown state. Used in public methods on the page object"""

class ExpectedElementError(Exception):
    """Raise this error when an element defies expectation. Used in private methods on the page object"""