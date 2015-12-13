# coding: utf-8
from unittest import TestCase
from selenium import webdriver
from helpers.pages.LoginForm.form_page import LoginForm


class DropboxLoginTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.dropbox.com/login")
        self.form_page = LoginForm(self.driver)

    def tearDown(self):
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
        form_page = self.form_page.form
        form_page.input_email('max@')
        form_page.submit_sing_in()  # «Войти»
        result = form_page.get_error_text()
        expect = ['Неверное название домена (часть адреса эл. почты после символа @: ).',
                  'The domain portion of the email address is invalid (the portion after the @: )']
        self.assertIn(result, expect)

    def test_empty_email_input(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/view/249
            1. Название: Поле ввода пустое, пробуем авторизироваться
            2. Предпосылки: зайти на сайт https://www.dropbox.com/login
            3. Шаги:
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Получаем ошибку «Введите свой адрес электронной почты»"""
        form_page = self.form_page.form
        form_page.wait_and_click_sing_in_button()
        result = form_page.get_error_text()
        expect = ['Введите свой адрес электронной почты.',
                  'Please enter your email']
        self.assertIn(result, expect)

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
        form_page = self.form_page.form
        form_page.input_email('макс@mail.ru')
        form_page.submit_sing_in()  # «Войти»
        result = form_page.get_error_text()
        expect = ['Введен неверный адрес электронной почты.',
                  'The e-mail you entered is invalid']
        self.assertIn(result, expect)

    def test_correct_email_and_empty_password(self):
        """Описание тест-кейса: https://projectt2015.testrail.net/index.php?/cases/view/272
            1. Название: Поле «Пароль» пустое, пробуем авторизоваться
            2. Предпосылки: зайти на сайт https://www.dropbox.com/login
            3. Шаги:
                - Ввести корректный адрес электронной почты.
                - Поставить галочку «Запомнить», если это необходимо
                - Нажать кнопку «Войти»
            4. Ожидаемый результат: Получаем ошибку «Введите пароль»"""
        form_page = self.form_page.form
        form_page.input_email('max@mail.ru')
        form_page.submit_sing_in()  # «Войти»
        result = form_page.get_error_text()
        expect = ['Введите пароль.',
                  'Please enter your password']
        self.assertIn(result, expect)

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
        form_page = self.form_page.form
        form_page.input_email('2gistestemail@mail.ru')
        form_page.input_pass('2gistestenter')
        form_page.submit_sing_in()  # «Войти»

        form_page.wait_page_elem('name')
        result = self.driver.find_element_by_css_selector('#header-account-menu > span > button > span.name').text
        expect = ['Maxim Kolesnikov']
        self.assertIn(result, expect)
