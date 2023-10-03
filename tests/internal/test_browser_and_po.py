import pytest
from selenium.webdriver.common.by import By

from tailored.driver import setup_chrome
from pages.base import BasePage

expected_links = [('Twitter', 'https://twitter.com/pyrva'),
                  ('GitHub', 'https://github.com/PyRVA'),
                  ('Meetup', 'http://www.meetup.com/PyRVAUserGroup/'),
                  ('Discord', 'https://discord.gg/fSGW7Jra4T'),
                  ('Meetup page', 'http://www.meetup.com/PyRVAUserGroup')]


def test_chrome_setup():
    driver = setup_chrome()
    driver.get('http://www.pyrva.org')
    assert [(e.text, e.get_attribute('href')) for e in driver.find_elements(By.TAG_NAME, 'a')] == expected_links


def test_abc_page_object():
    driver = setup_chrome()
    driver.get('http://www.pyrva.org')
    with pytest.raises(TypeError):
        generic_po = BasePage(driver)
