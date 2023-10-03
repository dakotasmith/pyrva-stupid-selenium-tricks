from pages.base import ExpectedElementError


class BaseElement:

    def __init__(self, locator):
        self.locator = locator

    def __get__(self, instance, owner):
        instance.wait_for_visibility(self.locator)
        element = instance.find_element(self.locator)
        return element.text


class InputElement(BaseElement):

    def __set__(self, instance, value):
        instance.wait_for_visibility(self.locator)
        element = instance.find_element(self.locator)
        try:
            element.send_keys(value)
        except AttributeError as exc:
            raise ExpectedElementError(
                f'could not send_keys to element - locator {self.locator}'
               ) from exc
        element.get_attribute('value')
