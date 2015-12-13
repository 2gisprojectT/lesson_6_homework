from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
        element = self.driver.find_element_by_css_selector("a.gb_Pd")
        link = element.get_attribute("href")
        self.driver.get(link)

        email = self.driver.find_element_by_id("Email")
        email.send_keys("lesson5homework")
        email_button = self.driver.find_element_by_id("next")
        email_button.submit()

        password = self.driver.find_element_by_id("Passwd")
        password.send_keys("projectt")
        password_button = self.driver.find_element_by_id("signIn")
        password_button.submit()

    def openMailForm(self):
        element = self.driver.find_element_by_css_selector("div.T-I.J-J5-Ji.T-I-KE.L3")
        element.click()

    def saveInDrafts(self):
        close = self.driver.find_element_by_css_selector("img.Ha")
        close.click()

    def sendMail(self):
        send = self.driver.find_element_by_css_selector("div.T-I.J-J5-Ji.aoO.T-I-atl.L3")
        send.click()

    def getSubjectOfLastMessage(self):
        divs = self.driver.find_elements_by_css_selector("div.BltHke.nH.oy8Mbf")
        for div in divs:
            if div.get_attribute("role") == "main":
                table = div.find_element_by_xpath("div/div/div/table")
                element = table.find_element_by_xpath("tbody/tr/td[6]/div/div/div/span")
                break
        return element.text

    def getSubjectOfLastMessageInDrafts(self):
        self.driver.get("https://mail.google.com/mail/#drafts")
        self.wait()
        return self.getSubjectOfLastMessage()

    def getSubjectOfLastMessageInSent(self):
        self.driver.get("https://mail.google.com/mail/#sent")
        self.wait()
        return self.getSubjectOfLastMessage()

    def wait(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.title_contains("wait_for_1_second")
            )
        except TimeoutException:
            return

    def testSubjectOfTheMessageIsEmpty(self):
        """ Моделирование ситуации, когда тема сообщения не введена
        Steps
            Нажать на пункт меню Написать
            Вводим имя пользователя - bstodin@gmail.com
            Оставляем тему сообщения пустой строкой
            Сохранить в черновиках
        Expected Result
            Письмо будет сохранено в черновиках, в качестве темы сообщения будет указано (без темы)."""
        self.openMailForm()
        receiver = self.driver.find_element_by_css_selector("textarea.vO")
        receiver.send_keys("lesson5homework@gmail.com")
        self.saveInDrafts()
        title = self.getSubjectOfLastMessageInDrafts()
        self.assertEqual("(без темы)", title)

    def testSubjectOfTheMessageIsCorrect(self):
        """ Моделирование ситуации, когда тема введена
        Steps
            Нажать на пункт меню Написать
            Вводим тему сообщения - "Тема сообщения"
            Сохранить в черновиках
        Expected Result
            Письмо будет сохранено в черновиках, в качестве темы сообщения "Тема сообщения"."""
        self.openMailForm()
        subject = self.driver.find_element_by_css_selector("input.aoT")
        subject.send_keys("Тема сообщения")
        self.saveInDrafts()
        title = self.getSubjectOfLastMessageInDrafts()
        self.assertEqual("Тема сообщения", title)

    def testReceiverOfTheMessageIsEmpty(self):
        """ Моделирование ситуации, когда получатель отстутствует
        Steps
            Нажать на пункт меню Написать
            Отправить
        Expected Result
            Письмо будет не будет отправлено, пользователь получит оповещение о том, что имя пользователя не введено."""
        self.openMailForm()
        self.sendMail()
        element = self.driver.find_element_by_css_selector("div.Kj-JD-Jz")
        self.assertEqual("Укажите как минимум одного получателя.", element.text)

    def testReceiverOfTheMessageIsCorrect(self):
        """ Моделирование ситуации, когда имя получателя введено корректно
        Steps
            Нажать на пункт меню Написать
            Вводим имя пользователя - lesson5homework@gmail.com и тему сообщения
            Отправить
        Expected Result
            Письмо будет успешно отправлено по адресу lesson5homework@gmail.com."""
        self.openMailForm()
        receiver = self.driver.find_element_by_css_selector("textarea.vO")
        receiver.send_keys("lesson5homework@gmail.com")
        subject = self.driver.find_element_by_css_selector("input.aoT")
        subject.send_keys("Письмо самому себе")
        self.sendMail()
        title = self.getSubjectOfLastMessageInSent()
        self.assertEqual("Письмо самому себе", title)

    def testReceiverOfTheMessageIsNotCorrect(self):
        """ Моделирование ситуации, когда имя получателя введено не корректно (отсутствует символ @)
        Steps
            Нажать на пункт меню Написать
            Вводим имя пользователя - lesson5homework_gmail.com
            Отправить
        Expected Result
            Письмо будет успешно отправлено по адресу lesson5homework@gmail.com."""
        self.openMailForm()
        receiver = self.driver.find_element_by_css_selector("textarea.vO")
        receiver.send_keys("lesson5homework_gmail.com")
        subject = self.driver.find_element_by_css_selector("input.aoT")
        subject.send_keys("Тема сообщения")
        self.sendMail()
        element = self.driver.find_element_by_css_selector("div.Kj-JD-Jz")
        self.assertEqual("Почтовый адрес \"\"lesson5homework_gmail.com\"\" не распознан. Исправьте его и повторите попытку.", element.text)
