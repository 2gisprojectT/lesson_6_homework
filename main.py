from unittest import TestCase
from selenium import webdriver
import time


class TestForMailGoogle(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://google.com/")
        self.driver.implicitly_wait(10)
        self.login()
        self.driver.get("http://mail.google.com/")

    def tearDown(self):
        self.driver.quit()

    def login(self):
        link = self.driver.find_element_by_css_selector("a.gb_Pd").get_attribute("href")
        self.driver.get(link)

        self.driver.find_element_by_id("Email").send_keys("lesson5homework")
        self.driver.find_element_by_id("next").submit()

        self.driver.find_element_by_id("Passwd").send_keys("projectt")
        self.driver.find_element_by_id("signIn").submit()

    def open_mail_form(self):
        self.driver.find_element_by_css_selector("div.T-I.J-J5-Ji.T-I-KE.L3").click()

    def save_in_drafts(self):
        self.driver.find_element_by_css_selector("img.Ha").click()

    def send_mail(self):
        self.driver.find_element_by_css_selector("div.T-I.J-J5-Ji.aoO.T-I-atl.L3").click()

    def get_subject_of_last_message(self):
        divs = self.driver.find_elements_by_css_selector("div.BltHke.nH.oy8Mbf")
        for div in divs:
            if div.get_attribute("role") == "main":
                table = div.find_element_by_xpath("div/div/div/table")
                element = table.find_element_by_xpath("tbody/tr/td[6]/div/div/div/span")
                break
        return element.text

    def get_subject_of_last_message_in_drafts(self):
        self.driver.get("https://mail.google.com/mail/#drafts")
        self.wait()
        return self.get_subject_of_last_message()

    def get_subject_of_last_message_in_sent(self):
        self.driver.get("https://mail.google.com/mail/#sent")
        self.wait()
        return self.get_subject_of_last_message()

    def wait(self):
        time.sleep(1)

    def test_subject_of_the_message_is_empty(self):
        """ Моделирование ситуации, когда тема сообщения не введена
        Steps
            Нажать на пункт меню Написать
            Вводим имя пользователя - bstodin@gmail.com
            Оставляем тему сообщения пустой строкой
            Сохранить в черновиках
        Expected Result
            Письмо будет сохранено в черновиках, в качестве темы сообщения будет указано (без темы)."""
        self.open_mail_form()
        self.driver.find_element_by_css_selector("textarea.vO").send_keys("lesson5homework@gmail.com")
        self.save_in_drafts()
        self.assertEqual("(без темы)", self.get_subject_of_last_message_in_drafts())

    def test_subject_of_the_message_is_correct(self):
        """ Моделирование ситуации, когда тема введена
        Steps
            Нажать на пункт меню Написать
            Вводим тему сообщения - "Тема сообщения"
            Сохранить в черновиках
        Expected Result
            Письмо будет сохранено в черновиках, в качестве темы сообщения "Тема сообщения"."""
        self.open_mail_form()
        self.driver.find_element_by_css_selector("input.aoT").send_keys("Тема сообщения")
        self.save_in_drafts()
        self.assertEqual("Тема сообщения", self.get_subject_of_last_message_in_drafts())

    def test_receiver_of_the_message_is_empty(self):
        """ Моделирование ситуации, когда получатель отстутствует
        Steps
            Нажать на пункт меню Написать
            Отправить
        Expected Result
            Письмо будет не будет отправлено, пользователь получит оповещение о том, что имя пользователя не введено."""
        self.open_mail_form()
        self.send_mail()
        self.assertEqual("Укажите как минимум одного получателя.",
                         self.driver.find_element_by_css_selector("div.Kj-JD-Jz").text)

    def test_receiver_of_the_message_is_correct(self):
        """ Моделирование ситуации, когда имя получателя введено корректно
        Steps
            Нажать на пункт меню Написать
            Вводим имя пользователя - lesson5homework@gmail.com и тему сообщения
            Отправить
        Expected Result
            Письмо будет успешно отправлено по адресу lesson5homework@gmail.com."""
        self.open_mail_form()
        self.driver.find_element_by_css_selector("textarea.vO").send_keys("lesson5homework@gmail.com")
        self.driver.find_element_by_css_selector("input.aoT").send_keys("Письмо самому себе")
        self.send_mail()
        self.assertEqual("Письмо самому себе", self.get_subject_of_last_message_in_sent())

    def test_receiver_of_the_message_is_not_correct(self):
        """ Моделирование ситуации, когда имя получателя введено не корректно (отсутствует символ @)
        Steps
            Нажать на пункт меню Написать
            Вводим имя пользователя - lesson5homework_gmail.com
            Отправить
        Expected Result
            Письмо будет успешно отправлено по адресу lesson5homework@gmail.com."""
        self.open_mail_form()
        self.driver.find_element_by_css_selector("textarea.vO").send_keys("lesson5homework_gmail.com")
        self.driver.find_element_by_css_selector("input.aoT").send_keys("Тема сообщения")
        self.send_mail()
        self.assertEqual("Почтовый адрес \"\"lesson5homework_gmail.com\"\" не распознан. Исправьте его и повторите попытку.",
                         self.driver.find_element_by_css_selector("div.Kj-JD-Jz").text)
