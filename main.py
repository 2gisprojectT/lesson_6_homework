"""пять тестов из набора тестов (unittest)"""

import unittest
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FiveTestsOfSuiteClass(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get('https://www.onetwotrip.com')


    def test_autocomplete(self):
        """ тест первый
        проверка автозаполнения

        заполняем первое поле "откуда"
        там вводим латинскими буквами неполное слово "novos"
        проверяем, чтобы система сама исправила его на "Новосибирск"
        """

        field_from = self.driver.find_element_by_name('from0')
        field_from.send_keys('novos')

        # ждем, когда в поле появится слово "Новосибирск"
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element_value((By.NAME, 'from0'), 'Новосибирск'))


    def test_incorrectly_specified_dates(self):
        """ тест второй
        проверка неверно заданных дат (дата прилета раньше даты вылета)

        заполняем первое поле "откуда", вводим Новосибирск
        заполняем второе поле "куда", вводим Москва
        в поле "туда" ставим 30 ноября
        в поле "обратно" ставим 29 ноября
        нажимаем на кнопку "Найти"
        должно выскочить окошко с предупреждением о том, что даты неверно заданы
        """

        field_from = self.driver.find_element_by_name('from0')
        field_from.send_keys('Новосибирск')

        field_to = self.driver.find_element_by_name('to0')
        field_to.send_keys('Москва')

        # 15 декабря
        self.driver.find_element_by_xpath("//*[contains(@Class,'1450116000000')]").click()

        # 13 декабря
        self.driver.find_element_by_name('date1').click()
        self.driver.find_element_by_xpath("//*[contains(@Class,'1449943200000')]").click()

        self.driver.find_element_by_name('submit').click()

        window_error = self.driver.find_element_by_class_name('wide_s').is_displayed()
        if (window_error == 1):
            text_error = self.driver.find_element_by_class_name('comment').text

        self.assertEqual(text_error, 'Неверно заданы даты')


    def test_control_data_after_click_button_change(self):
        """ тест третий
        проверка кнопки Изменить

        заполняем первое поле "откуда", вводим Новосибирск
        заполняем второе поле "куда", вводим Москва
        в поле "туда" выбираем дату (одну)
        нажимаем на кнопку "Найти"
        затем нажимаем на кнопку "Изменить", то есть вернуться к первоначальному запросу
        нужно проверить, что данные в полях сохранились.
        """

        text_from = 'Новосибирск'
        text_to = 'Москва'

        field_from = self.driver.find_element_by_name('from0')
        field_from.send_keys(text_from)

        field_to = self.driver.find_element_by_name('to0')
        field_to.send_keys(text_to)

        # 13 декабря
        self.driver.find_element_by_xpath("//*[contains(@Class,'1449943200000')]").click()
        text_date = self.driver.find_element_by_name('date0').get_attribute('value')

        self.driver.find_element_by_name('submit').click()

        self.driver.find_element_by_class_name('change').click()

        read_text_from = self.driver.find_element_by_name('from0').get_attribute('value')
        read_text_to = self.driver.find_element_by_name('to0').get_attribute('value')
        read_text_date = self.driver.find_element_by_name('date0').get_attribute('value')

        self.assertEqual(read_text_from, text_from)
        self.assertEqual(read_text_to, text_to)
        self.assertEqual(read_text_date, text_date)


    def test_check_result_of_search(self):
        """ тест четвертый
        проверка результата поиска

        заполняем первое поле "откуда", вводим Новосибирск
        заполняем второе поле "куда", вводим Москва
        выбираем дату (одну)
        нажимаем на кнопку "Найти"
        затем нажимаем на ссылку "подробнее"
        нужно проверить результаты поиска с введенными ранее данными
        """

        text_from = 'Новосибирск'
        text_to = 'Москва'

        field_from = self.driver.find_element_by_name('from0')
        field_from.send_keys(text_from)

        field_to = self.driver.find_element_by_name('to0')
        field_to.send_keys(text_to)

        # 13 декабря
        self.driver.find_element_by_xpath("//*[contains(@Class,'1449943200000')]").click()
        # будет записано - 30 Ноября, Пн
        text_date = self.driver.find_element_by_name('date0').get_attribute('value')

        self.driver.find_element_by_name('submit').click()

        self.driver.find_element_by_class_name('showTripInfo').click()

        # результат - Новосибирск с запятой, нужно запятую убрать
        res_text_from = self.driver.find_element_by_class_name('from').text
        # результат - Москва с запятой, нужно запятую убрать
        res_text_to = self.driver.find_element_by_class_name('to').text
        # результат - 30 ноя , причем с маленькой буквы...
        res_text_date = self.driver.find_element_by_class_name('date').text

        # выкинула запятую
        self.assertEqual(res_text_from[:-1], text_from)
        self.assertEqual(res_text_to[:-1], text_to)
        # сравниваю числа даты
        self.assertEqual(res_text_date[:2], text_date[:2])
        # сравниваю месяцы даты, достаточно проверить оя и оя, т.к. Ноя и ноя не могут быть равны
        self.assertEqual(res_text_date[4:6], text_date[4:6])


    def test_match_cities_in_field(self):
        """ тест пятый
        проверка невозможности выполнения запроса, в котором названия городов в полях совпадают

        заполняем первое поле "откуда", вводим Новосибирск
        заполняем второе поле "куда", вводим Новосибирск
        выбираем дату
        нажимаем на кнопку "Найти"
        нужно, чтобы выскочило окно с предупреждением о том, что пункты вылета и прилета совпадают.
        """

        field_from = self.driver.find_element_by_name('from0')
        field_from.send_keys('Новосибирск')

        field_to = self.driver.find_element_by_name('to0')
        field_to.send_keys('Новосибирск')

        # 13 декабря
        self.driver.find_element_by_xpath("//*[contains(@Class,'1449943200000')]").click()

        self.driver.find_element_by_name('submit').click()

        window_error = self.driver.find_element_by_class_name('wide_s').is_displayed()

        if (window_error == 1):
            text_error = self.driver.find_element_by_class_name('comment').text

        self.assertEqual(text_error, 'Неверно задан маршрут. Совпадают пункты вылета и прилёта.')


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
