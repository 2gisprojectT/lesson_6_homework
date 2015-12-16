import unittest
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutomaticTestCase(TestCase):

    def wait_element_by_id(self, element_id):
        element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, element_id)))
        return element

    def wait_element_by_class_name(self, element_class_name):
        element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, element_class_name)))
        return element

    def setUp(self):
        """
        Подготовка драйвера для тестирования основных действий
        """
        EMAIL = 'projecttfortest@gmail.com'# логин для входа, специально создан, можно пользоваться
        PASS = 'PasswordForTestAccount'    # корректный пароль, вход будет пройден

        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('feedly.com')

        self.driver.find_element_by_class_name('primary').click()
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.driver.find_element_by_class_name('google').click()

        login_field = self.driver.find_element_by_id('Email')
        login_field.send_keys(EMAIL)
        self.driver.find_element_by_id('next').click()

        pass_field = self.driver.find_element_by_id('Passwd')
        pass_field.send_keys(PASS)
        self.driver.find_element_by_id('signIn').click()
        self.driver.switch_to.window(handles[0])

    def tearDown(self):
        self.driver.close()

    def test_invalid_page_name_search(self): # Поиск по некорректному названию
        """Предусловия
        Для тестирования необходима учетная запись на сайте feedly.com.
        1. Перейти на сайт feedly.com, войти в учетную запись, нажав кнопку "Get started", выбрав способ входа и введя корректный логин и пароль.
        После проведения данных действий вы будете перенаправлены на страницу https://feedly.com/i/discover
        Шаги воспроизведения
        1. В строку поиска ввести, например, "sportbooooox.r" и нажать кнопку "Enter"
        Результат
        Нет доступных конопок "add" для добавления новостей
        """
        SEARCH_DATA = 'sportbooooox.ru'    # данные для поиска (есть возможность поиска по названию, тэгу и ссылке)

        search_field = self.wait_element_by_id('herculeInput')
        search_field.send_keys(SEARCH_DATA)
        search_field.send_keys(Keys.RETURN)

        error_page = self.driver.find_elements_by_class_name('simpleFollowButton')
        self.assertEqual(len(error_page),0)

    def test_delete_news(self): #Удаление новостей в существующем раздее
        """Предусловия
        Для тестирования необходима учетная запись на сайте feedly.com и ранее добавленный раздел новостей.
        1. Перейти на сайт feedly.com, войти в учетную запись, нажав кнопку "Get started", выбрав способ входа и введя корректный логин и пароль.
        После проведения данных действий вы будете перенаправлены на страницу https://feedly.com/i/discover
        Шаги воспроизведения
        1. Нажать на раздел левой кнопкой мыши - на странице будут отображены свежие новости раздела
        2. Нажать кнопку настройки раздела (Шестерёнку)
        3. Нажать "Remove"
        Результат
        Разделов с новостями на один меньше
        """
        design_button = self.wait_element_by_id('design_tab_label')
        design_tab = self.driver.find_element_by_id('design_tab_sources')
        design_sections = design_tab.find_elements_by_class_name('feedIndexTitleHolder')
        old_number = len(design_sections)

        design_sections[0].click()
        self.driver.find_element_by_id('pageActionCustomize').click()
        self.driver.find_element_by_id('unsubscribeAction').click()

        self.driver.refresh()
        design_button = self.wait_element_by_id('design_tab_label')
        design_tab = self.driver.find_element_by_id('design_tab_sources')
        new_design_sections = design_tab.find_elements_by_class_name('feedIndexTitleHolder')
        new_number = len(new_design_sections)

        self.assertEqual((old_number - new_number),1)

    def test_add_news_in_existing_section(self): # Добавление новостей в существующий раздел
        """Предусловия
        Для тестирования необходима учетная запись на сайте feedly.com.
        1. Перейти на сайт feedly.com, войти в учетную запись, нажав кнопку "Get started", выбрав способ входа и введя корректный логин и пароль.
        После проведения данных действий вы будете перенаправлены на страницу https://feedly.com/i/discover
        Шаги воспроизведения
        1. В строку поиска ввести, например, "sport" и нажать кнопку "Enter"
        2. В представленном списке выбрать раздел и нажать кнопку "+"
        3. В окне слева нажать кнопку "Add"
        Результат
        В результате в окне контента в разделе "Спорт" появится новый раздел, то есть количество разделов увеличится на 1
        """
        sport_tab = self.wait_element_by_id('sport_tab_sources')
        sport_sections = sport_tab.find_elements_by_class_name('feedIndex')
        old_number = len(sport_sections)

        SEARCH_DATA = 'sport'
        add_button = self.wait_element_by_class_name('secondaryPanelButton')
        add_button.click()
        search_field = self.wait_element_by_id('maxHerculeInput')
        search_field.send_keys(SEARCH_DATA)
        search_field.send_keys(Keys.RETURN)

        add_buttons = self.driver.find_elements_by_class_name('simpleFollowButton')
        add_buttons[0].click()
        self.driver.find_element_by_id('subscribe').click()

        self.driver.refresh()
        sport_tab = self.wait_element_by_id('sport_tab_sources')
        sport_sections = sport_tab.find_elements_by_class_name('feedIndex')
        new_number = len(sport_sections)

        self.assertEqual((new_number - old_number),1)

    def test_watch_news_on_primary_source_site(self): # Просмотр новостей на сайте-первоисточнике
        """Предусловия
        Для тестирования необходима учетная запись на сайте feedly.com и ранее добавленный раздел новостей.
        1. Перейти на сайт feedly.com, войти в учетную запись, нажав кнопку "Get started", выбрав способ входа и введя корректный логин и пароль.
        После проведения данных действий вы будете перенаправлены на страницу https://feedly.com/i/discover
        Шаги воспроизведения
        1. В окне отображения новостных разделов (полоса серого цвета в левой части страницы) нажать (например) кнопку "Советский спорт"
        2. Нажать кнопку настройки новостей (Шестерёнку)
        3. Нажать опцию "Open on website directory"
        4. Выбрать новость
        Результат
        В результате откроется новое окно с сайтом-первоисточником новости
        """
        sport_tab = self.wait_element_by_id('sport_tab_sources')
        sport_sections = sport_tab.find_elements_by_class_name('feedIndex')

        sport_sections[0].click()
        self.driver.find_element_by_id('pageActionCustomize').click()
        action_buttons = self.driver.find_elements_by_class_name('action')
        for attribute in action_buttons:
            if (attribute.get_attribute('data-page-action') == 'toggleCurrentSubscriptionOpenInWebsiteDirectly'):
                attribute.click()
                break
        sport_articles = self.driver.find_elements_by_class_name('unread')
        id_temp = sport_articles[0].get_attribute('id')
        self.driver.find_element_by_id(id_temp).click()

        new_handles = self.driver.window_handles
        self.driver.switch_to.window(new_handles[1])

        self.driver.find_element_by_class_name('facebook-bn_close-btn').click()
        self.driver.find_element_by_class_name('site-logo').click()
        site_name = self.driver.current_url
        self.assertEqual(site_name,'http://www.sovsport.ru/')

    def test_full_article_picture(self): # Проверка полного описания новостного контента
        """Предусловия
        Для тестирования необходима учетная запись на сайте feedly.com и ранее добавленный раздел новостей.
        1. Перейти на сайт feedly.com, войти в учетную запись, нажав кнопку "Get started", выбрав способ входа и введя корректный логин и пароль.
        После проведения данных действий вы будете перенаправлены на страницу https://feedly.com/i/discover
        Шаги воспроизведения
        1. В окне отображения новостных разделов (полоса серого цвета в левой части страницы) нажать кнопку "All"
        2. Нажать кнопку настройки всех новостей (Шестерёнку)
        3. В пункте "Presentation" выбрать пункт "Full articles"
        Результат
        Новости располагаются столбцом, при этом каждая новость обрамлена, отображается видео, если оно приложено, есть краткое описание и возможность поделиться в соц. сетях
        Комментарий: в качестве проверки правильности используется поиск кнопки "Visit Website", которая присутствует только в данном представлении
        """
        all_button = self.wait_element_by_id('feedlyTab')
        all_button.find_element_by_id('latesttab_label').click()
        self.driver.find_element_by_id('pageActionCustomize').click()
        self.driver.find_element_by_id('lvc_u100').click()
        visit_buttons = self.driver.find_elements_by_class_name('websiteCallForAction')
        self.assertNotEqual(len(visit_buttons),0)
