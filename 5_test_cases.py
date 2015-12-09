# coding: utf-8
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.dropbox.com/login")

    def tearDown(self):
        self.assertIn(self.result, self.expect)
        self.driver.quit()

    def test_email_without_domain_name(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/edit/253
            1. Название: Поле ввода содержит знак «@» и корректные знаки перед ним, но не содержит доменное имя, пробуем
             авторизоваться
            2. Предпосылки: зайти на сайт https://www.dropbox.com/login
            3. Шаги:
                - Ввести адрес электронной почты без доменного имени, например «max@»
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Получаем ошибку «Неверное название домена (часть адреса эл. почты после символа @:
            ).»"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-input-input")))
        element.send_keys('max@')

        self.driver.find_element_by_class_name('login-button').click()  # «Войти»
        self.result = self.driver.find_element_by_class_name('error-message').text
        self.expect = ['Неверное название домена (часть адреса эл. почты после символа @: ).',
                       'The domain portion of the email address is invalid (the portion after the @: )']

    def test_empty_email_input(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/view/249
            1. Название: Поле ввода пустое, пробуем авторизироваться
            2. Предпосылки: зайти на сайт https://www.dropbox.com/login
            3. Шаги:
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Получаем ошибку «Введите свой адрес электронной почты»"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'login-button')))
        element.click()     # «Войти»

        self.result = self.driver.find_element_by_class_name('error-message').text
        self.expect = ['Введите свой адрес электронной почты.',
                       'Please enter your email']

    def test_impossible_email(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/view/251
            1. Название: Поле ввода содержит кириллицу перед знаком «@» и корректное доменное имя, пробуем
        авторизироваться
            2. Предпосылки: зайти на сайт https://www.dropbox.com/login
            3. Шаги:
                - Ввести адрес электронной почты с содержанием кириллицы в имени почты например макс@mail.ru
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Получаем ошибку «Введен неверный адрес электронной почты.»"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-input-input")))
        element.send_keys('макс@mail.ru')

        self.driver.find_element_by_class_name('login-button').click()  # «Войти»
        self.result = self.driver.find_element_by_class_name('error-message').text
        self.expect = ['Введен неверный адрес электронной почты.',
                       'The e-mail you entered is invalid']

    def test_correct_email_and_empty_password(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/view/272
            1. Название: Поле «Пароль» пустое, пробуем авторизоваться
            2. Предпосылки: зайти на сайт https://www.dropbox.com/login
            3. Шаги:
                - Ввести корректный адрес электронной почты.
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Получаем ошибку «Введите пароль»"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-input-input")))
        element.send_keys('max@mail.ru')

        self.driver.find_element_by_class_name('login-button').click()  # «Войти»
        self.result = self.driver.find_element_by_class_name('error-message').text
        self.expect = ['Введите пароль.',
                       'Please enter your password']

    def test_entered_when_input_data_correct(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/view/230
            1. Название: Успешная авторизация без автозаполнения
            2. Предпосылки:
                - Зайти на сайт https://www.dropbox.com/login
                - Быть зарегистрированным и знать данные для полей «Адрес электронной почты» и «Пароль».
            3. Шаги:
                - Корректно заполнить поля «Адрес электронной почты» и «Пароль»
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Успешная авторизация пользователя, узнаем имя пользователя"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'text-input-input')))
        element.send_keys('2gistestemail@mail.ru')

        self.driver.find_element_by_class_name('password-input').send_keys('2gistestenter')
        self.driver.find_element_by_class_name('login-button').click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'name')))
        self.result = self.driver.find_element_by_css_selector('#header-account-menu > span > button > span.name').text
        self.expect = ['Maxim Kolesnikov']
