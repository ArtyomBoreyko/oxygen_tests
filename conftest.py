"""
Общие фикстуры для тестов Selenium.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """
    Инициализация WebDriver для Chrome.
    Используется во всех тестах.
    """
    try:
        # Настройка опций Chrome
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Используем Selenium Manager (встроенный в Selenium 4.6+) для автоматического подбора драйвера
        # Это решает проблему с несовместимостью версий
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        yield driver
        
        driver.quit()
    except Exception as e:
        pytest.fail(f"Ошибка при инициализации WebDriver: {str(e)}\n"
                   f"Убедитесь, что установлена последняя версия Google Chrome.\n"
                   f"Попробуйте обновить зависимости: pip install --upgrade selenium")

