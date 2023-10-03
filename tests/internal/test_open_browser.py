from selenium.webdriver.common.by import By

from tailored.driver import setup_chrome


def test_chrome_setup():
    expected_links = [('Twitter', 'https://twitter.com/pyrva'),
                      ('GitHub', 'https://github.com/PyRVA'),
                      ('Meetup', 'http://www.meetup.com/PyRVAUserGroup/'),
                      ('Discord', 'https://discord.gg/fSGW7Jra4T'),
                      ('Meetup page', 'http://www.meetup.com/PyRVAUserGroup')]
    driver = setup_chrome()
    driver.get('http://www.pyrva.org')
    assert [(e.text, e.get_attribute('href')) for e in driver.find_elements(By.TAG_NAME, 'a')] == expected_links
