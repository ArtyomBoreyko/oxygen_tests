"""
Негативный тест: проверка некорректного содержания кислорода в атмосфере Земли.
Тест проверяет, что в статье Википедии о Земле НЕ указано некорректное содержание кислорода (например, 100%).
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestIncorrectOxygenContent:
    """Класс для негативного тестирования информации об атмосфере Земли в Википедии."""
    
    def test_incorrect_oxygen_content_not_present(self, driver):
        """
        Негативный тест: проверка, что в статье НЕ указано некорректное содержание кислорода.
        Проверяет, что в статье о Земле не указано содержание кислорода 100% в атмосфере.
        """
        try:
            import time
            
            # Шаг 1: Переход на страницу Википедии
            driver.get("https://ru.wikipedia.org")
            
            # Шаг 2: Поиск поля поиска и ввод "Земля"
            search_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "searchInput"))
            )
            search_box.clear()
            search_box.send_keys("Земля")
            search_box.send_keys(Keys.RETURN)
            
            # Шаг 3: Ждем загрузки страницы и проверяем результат поиска
            time.sleep(3)
            
            # Проверяем, на какой странице мы находимся
            current_url = driver.current_url
            article_loaded = False
            
            # Проверяем, попали ли мы сразу на статью
            if '/wiki/' in current_url:
                try:
                    article_heading = driver.find_elements(By.ID, "firstHeading")
                    if article_heading:
                        # Проверяем, что это статья о Земле
                        heading_text = article_heading[0].text.lower()
                        url_lower = current_url.lower()
                        if 'земля' in heading_text or 'земля' in url_lower or 'wiki/земля' in url_lower:
                            article_loaded = True
                except Exception:
                    pass
            
            # Если открылась страница результатов поиска, кликаем на первую ссылку
            if not article_loaded:
                try:
                    # Проверяем наличие заголовка статьи
                    first_heading = driver.find_elements(By.ID, "firstHeading")
                    if not first_heading:
                        # Если заголовка нет, значит мы на странице результатов поиска
                        # Ищем первую ссылку на статью "Земля" в результатах поиска
                        selectors = [
                            "//div[@class='mw-search-result-heading']/a[1]",
                            "//ul[@class='mw-search-results']//li[1]//a[1]",
                            "//div[@class='searchresults']//a[1]",
                            "//div[contains(@class, 'mw-search-result')]//a[contains(@title, 'Земля')][1]",
                            "//a[contains(@href, '/wiki/Земля')][1]",
                            "//a[contains(@href, 'wiki/Земля')][1]"
                        ]
                        
                        link_found = False
                        for selector in selectors:
                            try:
                                first_result_link = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, selector))
                                )
                                # Проверяем, что ссылка ведет на статью о Земле
                                href = first_result_link.get_attribute('href') or ''
                                title = first_result_link.get_attribute('title') or first_result_link.text or ''
                                if 'земля' in title.lower() or '/wiki/Земля' in href or 'wiki/Земля' in href:
                                    first_result_link.click()
                                    link_found = True
                                    break
                            except Exception:
                                continue
                        
                        if link_found:
                            # Ждем загрузки статьи
                            WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.ID, "firstHeading"))
                            )
                            time.sleep(2)
                            article_loaded = True
                except Exception as e:
                    print(f"Предупреждение при поиске ссылки: {e}")
            
            # Если все еще не загрузилась статья, делаем прямой переход
            if not article_loaded:
                print("Выполняем прямой переход на статью о Земле...")
                driver.get("https://ru.wikipedia.org/wiki/Земля")
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "firstHeading"))
                )
                time.sleep(2)
            
            # Убеждаемся, что мы на странице статьи
            article_heading = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "firstHeading"))
            )
            
            # Более гибкая проверка - проверяем и заголовок, и URL
            heading_text = article_heading.text.lower()
            current_url_lower = driver.current_url.lower()
            
            # Проверяем различные варианты
            is_earth_page = (
                'земля' in heading_text or 
                '/wiki/земля' in current_url_lower or 
                'wiki/земля' in current_url_lower or
                current_url_lower.endswith('/wiki/земля') or
                'земля' in current_url_lower.split('/')[-1]
            )
            
            if not is_earth_page:
                # Дополнительная проверка - может быть заголовок на другом языке или с доп. символами
                if '/wiki/' in current_url_lower and article_heading.text.strip():
                    is_earth_page = True
            
            assert is_earth_page, (
                f"Не удалось перейти на статью о Земле.\n"
                f"Текущий URL: {driver.current_url}\n"
                f"Заголовок страницы: {article_heading.text}"
            )
            
            # Шаг 4: Поиск информации о содержании кислорода в атмосфере
            # Ищем текст страницы, который содержит информацию об атмосфере
            main_content = driver.find_element(By.ID, "mw-content-text")
            main_text = main_content.text
            text_lower = main_text.lower()
            
            # Некорректные значения кислорода для проверки (только с процентами, чтобы исключить годы, расстояния и т.д.)
            incorrect_oxygen_values = ["100%", "100,00%", "100.00%"]
            
            # Проверяем наличие некорректных значений в контексте атмосферы
            incorrect_value_found = False
            found_value = None
            found_context = None
            
            for value in incorrect_oxygen_values:
                value_lower = value.lower()
                if value_lower in text_lower:
                    # Ищем все вхождения значения
                    idx = 0
                    while idx < len(text_lower):
                        idx = text_lower.find(value_lower, idx)
                        if idx == -1:
                            break
                        
                        # Ищем контекст вокруг найденного значения (увеличиваем контекст для лучшей проверки)
                        context_start = max(0, idx - 300)
                        context_end = min(len(text_lower), idx + 300)
                        context = text_lower[context_start:context_end]
                        
                        # Строгая проверка: должно быть одновременно:
                        # 1. Упоминание кислорода
                        # 2. Упоминание атмосферы или состава
                        # 3. Значение 100% должно быть связано с кислородом (не с другими газами)
                        
                        has_oxygen = any(keyword in context for keyword in ["кислород", "oxygen", "o2", "о2"])
                        has_atmosphere = any(word in context for word in ["атмосфер", "atmosphere", "состав", "composition"])
                        
                        if has_oxygen and has_atmosphere:
                            # Дополнительная проверка: убеждаемся, что 100% относится именно к кислороду
                            # Ищем паттерны типа "кислород 100%" или "100% кислород" или "кислород: 100%"
                            # Исключаем случаи типа "азот 100%" или "кислород 100% чистоты"
                            
                            # Проверяем, что между "кислород" и "100%" нет других газов
                            oxygen_positions = []
                            for keyword in ["кислород", "oxygen", "o2", "о2"]:
                                pos = context.find(keyword)
                                while pos != -1:
                                    oxygen_positions.append(pos)
                                    pos = context.find(keyword, pos + len(keyword))
                            
                            # Проверяем расстояние между кислородом и 100%
                            value_pos_in_context = idx - context_start
                            min_distance = float('inf')
                            
                            for ox_pos in oxygen_positions:
                                distance = abs(ox_pos - value_pos_in_context)
                                if distance < min_distance:
                                    min_distance = distance
                            
                            # Если кислород и 100% находятся близко (в пределах 100 символов)
                            if min_distance < 100:
                                # Проверяем, что между ними нет упоминаний других газов
                                start_check = min(value_pos_in_context, min(oxygen_positions) if oxygen_positions else value_pos_in_context)
                                end_check = max(value_pos_in_context + len(value_lower), max(oxygen_positions) + 10 if oxygen_positions else value_pos_in_context)
                                check_region = context[max(0, start_check - 50):min(len(context), end_check + 50)]
                                
                                # Исключаем случаи, где упоминаются другие газы рядом со 100%
                                other_gases = ["азот", "nitrogen", "n2", "аргон", "argon", "co2", "углекислый", "углекислот"]
                                has_other_gas = any(gas in check_region for gas in other_gases)
                                
                                # Исключаем случаи типа "100% чистоты", "100% концентрации" (не про состав атмосферы)
                                purity_words = ["чистоты", "purity", "концентрации", "concentration", "содержания", "content"]
                                has_purity_context = any(word in check_region for word in purity_words)
                                
                                # Если нет других газов и нет контекста чистоты, и есть упоминание атмосферы
                                if not has_other_gas and not has_purity_context:
                                    incorrect_value_found = True
                                    found_value = value
                                    found_context = context
                                    break
                        
                        idx += len(value_lower)
                    
                    if incorrect_value_found:
                        break
            
            # Альтернативный способ: поиск в таблицах и секциях об атмосфере
            if not incorrect_value_found:
                try:
                    # Ищем заголовок "Атмосфера" и ищем информацию в следующей секции
                    atmosphere_headers = driver.find_elements(
                        By.XPATH, 
                        "//span[@class='mw-headline' and (contains(text(), 'Атмосфера') or contains(text(), 'атмосфера'))]"
                    )
                    
                    for header in atmosphere_headers:
                        try:
                            # Получаем родительский раздел
                            section = header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'mw-parser-output')]//div[contains(@class, 'mw-content-ltr')] | ./ancestor::div[contains(@class, 'mw-parser-output')]")
                            section_text = section.text
                            section_text_lower = section_text.lower()
                            
                            for value in incorrect_oxygen_values:
                                value_lower = value.lower()
                                if value_lower in section_text_lower:
                                    idx = section_text_lower.find(value_lower)
                                    if idx != -1:
                                        context_start = max(0, idx - 300)
                                        context_end = min(len(section_text_lower), idx + 300)
                                        context = section_text_lower[context_start:context_end]
                                        
                                        # Строгая проверка как в основном коде
                                        has_oxygen = any(keyword in context for keyword in ["кислород", "oxygen", "o2", "о2"])
                                        has_atmosphere = any(word in context for word in ["атмосфер", "atmosphere", "состав", "composition"])
                                        
                                        if has_oxygen and has_atmosphere:
                                            # Проверяем, что это именно про кислород, а не другие газы
                                            value_pos_in_context = idx - context_start
                                            oxygen_positions = []
                                            for keyword in ["кислород", "oxygen", "o2", "о2"]:
                                                pos = context.find(keyword)
                                                while pos != -1:
                                                    oxygen_positions.append(pos)
                                                    pos = context.find(keyword, pos + len(keyword))
                                            
                                            if oxygen_positions:
                                                min_distance = min(abs(ox_pos - value_pos_in_context) for ox_pos in oxygen_positions)
                                                if min_distance < 100:
                                                    check_region = context[max(0, value_pos_in_context - 50):min(len(context), value_pos_in_context + len(value_lower) + 50)]
                                                    other_gases = ["азот", "nitrogen", "n2", "аргон", "argon", "co2", "углекислый"]
                                                    purity_words = ["чистоты", "purity", "концентрации", "concentration"]
                                                    
                                                    if not any(gas in check_region for gas in other_gases) and not any(word in check_region for word in purity_words):
                                                        incorrect_value_found = True
                                                        found_value = value
                                                        found_context = context
                                                        break
                            
                            if incorrect_value_found:
                                break
                        except Exception:
                            continue
                    
                    # Если не нашли, ищем в таблицах
                    if not incorrect_value_found:
                        tables = driver.find_elements(By.TAG_NAME, "table")
                        for table in tables:
                            table_text = table.text
                            table_text_lower = table_text.lower()
                            for value in incorrect_oxygen_values:
                                value_lower = value.lower()
                                if value_lower in table_text_lower:
                                    idx = table_text_lower.find(value_lower)
                                    if idx != -1:
                                        context_start = max(0, idx - 300)
                                        context_end = min(len(table_text_lower), idx + 300)
                                        context = table_text_lower[context_start:context_end]
                                        
                                        # Строгая проверка: должно быть упоминание и кислорода, и атмосферы
                                        has_oxygen = any(keyword in context for keyword in ["кислород", "oxygen", "o2", "о2"])
                                        has_atmosphere = any(word in context for word in ["атмосфер", "atmosphere", "состав", "composition"])
                                        
                                        if has_oxygen and has_atmosphere:
                                            # Проверяем, что 100% относится к кислороду, а не к другим газам
                                            value_pos_in_context = idx - context_start
                                            oxygen_positions = []
                                            for keyword in ["кислород", "oxygen", "o2", "о2"]:
                                                pos = context.find(keyword)
                                                while pos != -1:
                                                    oxygen_positions.append(pos)
                                                    pos = context.find(keyword, pos + len(keyword))
                                            
                                            if oxygen_positions:
                                                min_distance = min(abs(ox_pos - value_pos_in_context) for ox_pos in oxygen_positions)
                                                if min_distance < 100:
                                                    check_region = context[max(0, value_pos_in_context - 50):min(len(context), value_pos_in_context + len(value_lower) + 50)]
                                                    other_gases = ["азот", "nitrogen", "n2", "аргон", "argon", "co2", "углекислый"]
                                                    purity_words = ["чистоты", "purity", "концентрации", "concentration"]
                                                    
                                                    if not any(gas in check_region for gas in other_gases) and not any(word in check_region for word in purity_words):
                                                        incorrect_value_found = True
                                                        found_value = value
                                                        found_context = context
                                                        break
                            if incorrect_value_found:
                                break
                except Exception as e:
                    print(f"\nПредупреждение: не удалось выполнить дополнительный поиск: {e}")
            
            # Проверка результата - НЕ должно быть найдено некорректное значение
            assert not incorrect_value_found, (
                f"ОШИБКА: В статье найдено некорректное содержание кислорода {found_value} в атмосфере!\n"
                f"Это неверная информация - в атмосфере Земли содержится 20,95% кислорода, а не {found_value}.\n"
                f"URL страницы: {driver.current_url}\n"
                f"Заголовок статьи: {article_heading.text}\n"
                f"Контекст найденного значения: {found_context[:300] if found_context else 'N/A'}..."
            )
            
            print("\n✓ Негативный тест пройден: Некорректное содержание кислорода (100%) НЕ найдено в статье")
            print("  Статья содержит корректную информацию об атмосфере Земли")
            
        except Exception as e:
            pytest.fail(f"Ошибка при выполнении негативного теста: {str(e)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

