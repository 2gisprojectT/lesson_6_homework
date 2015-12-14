# coding: windows-1251
import unittest
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestRegistrationForm(TestCase):

    """Тестирование формы регистрации сайта "2gis.ru" """

    def setUp(self):
        """
        Открытие страницы регистрации в браузере Firefox
        """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get('http://2gis.ru/novosibirsk/auth/signup')

    def testing_links_to_the_license_agreement(self):
        """
        Тестирование ссылки "С пользовательским соглашением ознакомился и согласен":

        1. Нажать на ссылку "с пользовательским соглашением ознакомился и согласен".

        Expected Result
        Появление текста пользовательского соглашения в этом же окне, либо в новом.
        """

        text_checkbox = self.driver.find_element_by_class_name('auth__popup')
        link_to_the_license_agreement = text_checkbox.find_element_by_link_text('пользовательским соглашением')
        link_to_the_license_agreement.click()

        names_windows = self.driver.window_handles
        self.driver.switch_to.window(names_windows[1])

        self.assertIn("licensing", str(self.driver.current_url))

    def testing_link_authorization_vk(self):
        """
        Тестирование ссылки на авторизацию через "vk.com":
        1. Нажать на линк с ссылкой на vk.com.

        Expected Result
        Открытие сайта vk.com и появление формы запроса на разрешение доступа к аккаунту.
        """

        link_vk = self.driver.find_element_by_css_selector('li.auth__popupSocialItem:nth-child(1)')
        link_vk.click()

        names_windows = self.driver.window_handles
        self.driver.switch_to.window(names_windows[1])
        self.assertIn("oauth", str(self.driver.current_url))

    def test_the_password_field(self):
        """
        Тестирование формы регистрации с пустым паролем:
        1. Ввести в поле для электронной почты "test@mail.ru".
        2. Оставить поле для ввода пароля пустым.
        3. Поставить галочку в чекбоксе "С пользовательским соглашением ознакомился и согласен".

        Expected Result
        Кнопка "Зарегистрироваться" не активирована, регистрация не произведена, пользователь не записан в базу данных.
        При попытке нажать кнопку "Зарегистрироваться" появляется сообщение об ошибке "Вы не ввели пароль!".
        """

        email = self.driver.find_element_by_css_selector('.auth__formFieldEmail')
        email.send_keys('test@mail.ru')

        checkbox = self.driver.find_element_by_class_name('auth__formFieldPseudocheckbox')
        checkbox.click()

        class_names = str(self.driver.find_element_by_css_selector('.auth__formSubmitBtn').get_attribute('class'))
        if class_names.find('_disabled') == -1:
            button_is_not_active = True
        else:
            button_is_not_active = False

        self.assertFalse(button_is_not_active)

    def testing_cooperation_fields_checkbox_is_empty(self):
        """
        Общее тестирование формы. Поля "Электронный адрес" и "Пароль" заполненны ВЕРНО, при том, что галочка в чек-боксе ОТСУТСТВУЕТ:
        1. Ввести в поле для электронной почты "test@mail.ru".
        2. Ввести в поле для пароля "test123".
        3. Проверить, что галочка в чек-боксе "с пользовательским соглашения ознакомился и согласен" ОТСУТСТВУЕТ.
        4. Нажать кнопку "Зарегистрироваться".

        Expected Result
        Регистрация не произведена, пользователь не записан в базу данных.
        Сообщение об ошибке "Вы должны принять лицензионное соглашение".
        """

        email = self.driver.find_element_by_css_selector('.auth__formFieldEmail')
        email.send_keys('test@mail.ru')

        password = self.driver.find_element_by_css_selector('.auth__formFieldPassword')
        password.send_keys('test123')

        button_reg = self.driver.find_element_by_class_name('auth__formSubmitBtn')
        button_reg.click()

        class_names = str(self.driver.find_element_by_class_name('auth__popup').get_attribute('class'))
        if class_names.find('_error') == -1:
            error = True
        else:
            error = False
        self.assertFalse(error)

    def testing_cooperation_fields_checkbox_filled(self):
        """
        Общее тестирование формы. Поля "Электронный адрес" и "Пароль" заполненны ВЕРНО, при том, что галочка в чек-боксе ПОСТАВЛЕНА:
        1. Ввести в поле "Электронная почта" "test@mail.ru"
        2. Ввести в поле для пароля "test12345".
        3. Поставить галочку в боксе "С пользовательским соглашением ознакомился и согласен".
        4. Нажать кнопку "Зарегистрироваться".

        Expected Result
        Регистрация пройдена, пользователь записан в базу данных. На email отправлено письмо об успешной регистрации.
        """

        self.driver.find_element_by_css_selector('.auth__formFieldEmail').send_keys('test12345@mail.ru')

        password = self.driver.find_element_by_css_selector('.auth__formFieldPassword')
        password.send_keys('test123')

        checkbox = self.driver.find_element_by_class_name('auth__formFieldPseudocheckbox')
        checkbox.click()

        button_reg = self.driver.find_element_by_class_name('auth__formSubmitBtn')
        button_reg.click()

        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'auth__popup'), 'Подтверждение e-mail'))

    def tearDown(self):
        """
        Закрытие страницы браузера
        """
        self.driver.quit()

if __name__ == "__main__":

    unittest.main()
