import unittest

from selenium import webdriver
from selenium.webdriver.support.select import Select


class FirstTestCase(unittest.TestCase):
    def setUp(self):
        """
        Prescriptions:
            1.Login in the site with your email and password.
            2.Go to your profile.
        """
        self.user_email = "i1429637@trbvm.com"
        self.user_password = "projectt"
        self.user_first_name = "Anton"
        self.user_country = {u"Сингапур": "SG"}

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get("https://www.onetwotrip.com")

        self.driver.find_element_by_class_name("enter").click()
        register_email_field = self.driver.find_element_by_name("auth_email")
        register_password_field = self.driver.find_element_by_name("auth_pas")

        register_email_field.send_keys(self.user_email)
        register_password_field.send_keys(self.user_password)
        self.driver.find_element_by_class_name("pos_but").click()

        self.driver.find_element_by_class_name("knownUser").click()
        self.assertEqual(u"Профиль покупателя",
                         self.driver.find_element_by_id("pageTitle").text)

    def test_input_correct_last_name(self):
        """
        Steps:
            1.Input last name in 'First Name' field.
            2.Push the 'Save changes' button.
            3.Refresh the current page.
        """
        driver = self.driver

        first_name_field = driver.find_element_by_id("input_firstName")
        first_name_field.send_keys(self.user_first_name)
        driver.find_element_by_id("button_saveContacts").click()

        driver.refresh()

        """
        Expected result:
            The entered name was retained in the field.
        """
        introduced_last_name = first_name_field.get_attribute("value")
        self.assertEqual(introduced_last_name, self.user_first_name)

    def test_go_to_hotels_page(self):
        """
        Steps:
            1.Push the 'Find a hotel' button.
            2.Check transition.
        """
        driver = self.driver

        """ итак, СУПЕР браузер Mozilla при нажатии на кнопку (с переходом на ссылку) открывает новую вкладку в НОВОМ окне
            (т.е. дублирует браузер и там открывает вкладку) следовательно у меня есть несколько путей решения этой проблемы:
            1.Передавать свои настройки в браузер, чтобы открывать вкладку в текущем окне - http://stackoverflow.com/questions/24054404/how-to-change-firefox-settings-in-webdriver-test
            2.Переключаться между окнами посредством ActionChains - http://stackoverflow.com/questions/28715942/how-do-i-switch-to-the-active-tab-in-selenium
            3.Переключать фокус между окнами с помощью switch_to - мой выбор, правильно или нет это вопрос
        """
        driver.find_element_by_xpath("//*[@id='hotelCompare']").click()
        driver.switch_to.window(driver.window_handles[1])

        """
        Expected result:
            The transition took place.
        """
        self.assertIn("hotels", str(driver.current_url))

    def test_autocomplete_email_field(self):
        """
        Steps:
            1.Check the 'email' field after autocomplete
        """
        driver = self.driver

        user_email_autocomplete = driver.find_element_by_xpath("//*[@id='form_contacts']/div[1]/div[2]/div").text

        """
        Expected result:
            The email was autocomplete.
        """
        self.assertEqual(user_email_autocomplete,
                         self.user_email)

    def test_select_country(self):
        """
        Steps:
            1.Select country in the 'Country' field
            2.Check the 'Country' field
        """
        driver = self.driver
        user_country_field = driver.find_element_by_name("country")

        selected_user_country = Select(user_country_field)
        selected_user_country.select_by_value(self.user_country.get(u"Сингапур"))

        """
        Expected result:
            The selected country retained in the field.
        """
        self.assertEqual(user_country_field.get_attribute("value"),
                         self.user_country.get(u"Сингапур"))

    def test_add_empty_passenger_to_address_book(self):
        """
        Steps:
            1.Push the 'Add Passenger' button.
            2.Push the 'Save Changes' button.
            3.Check the 'Save Changes' button status (Displayed).
        """
        driver = self.driver

        save_button = driver.find_element_by_id("button_addPassenger")
        save_button.click()
        driver.find_element_by_id("button_savePassengers").click()

        """
        Expected result:
            The "Save" button is displayed on the screen.
        """
        self.assertTrue(save_button.is_displayed())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
