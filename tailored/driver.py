import json
from contextlib import suppress
from os import path, getenv

from selenium.webdriver import Chrome, ChromeOptions


def find_responses_by_url(url, logs):
    """
    Returns a response object from the performance log msgs
    :param url: (partial) url to search
    :param logs: Browser driver logs

    :return: The response matching the (partial) url
    """
    for log in logs:
        if log['message']:
            data = json.loads(log['message'])
            with suppress(KeyError):
                if url in data['message']['params']['response']['url']:
                    return data['message']['params']['response']
    raise ValueError(f'Error finding response for url {url}')


def setup_chrome(profile='Default'):

    dl_path = path.abspath('dl')
    browser_mode = getenv('BROWSER_MODE', 'headless')
    headless: bool = browser_mode == 'headless'
    profiles_dir = path.abspath('.profiles')
    profile_path = path.join(profiles_dir, profile)

    # browser options
    gui_options = {
        'arguments': [
            '--disable-popup-blocking',
            '--disable-notifications',
            '--force-renderer-accessibility',
            '--ignore-certificate-errors'
        ],
        'experimental': [
            ('excludeSwitches', ['enable-automation', 'enable-logging'])
        ]
    }

    headless_options = {
        'arguments': ['--headless=new']
    }

    profile_options = {
        'arguments': [
            f'user-data-dir={profile_path}'
        ]
    }

    shared_options = {
        'arguments': [
            '--disable-blink-features=AutomationControlled',
            '--disable-extensions',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-sandbox',
            '--window-size=1920x1080'
        ],
        'experimental': [
            ('prefs', {
                'download.default_directory': dl_path,
                'download.prompt_for_download': False,
                'credentials_enable_service': False,
                'profile.password_manager_enabled': False
            },
             ('useAutomationExtension', False)
             )
        ],
        'capability': [('goog:loggingPrefs', {'performance': 'ALL'})],
    }

    if headless:
        base_options = headless_options
    else:
        base_options = gui_options

    options = [base_options, profile_options, shared_options]

    chrome_options = ChromeOptions()

    while options:
        option_group = options.pop()
        for argument in option_group['arguments']:
            chrome_options.add_argument(argument)
        with suppress(KeyError):
            for ex_op in option_group['experimental']:
                chrome_options.add_experimental_option(ex_op[0], ex_op[1])
        with suppress(KeyError):
            for capability in option_group['capability']:
                chrome_options.set_capability(capability[0], capability[1])

    driver = Chrome(options=chrome_options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # remove automation only item

    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': dl_path}
    }

    driver.command_executor._commands['send_command'] = (
        'POST',
        '/session/$sessionId/chromium/send_command'
    )
    _ = driver.execute('send_command', params)
    return driver
