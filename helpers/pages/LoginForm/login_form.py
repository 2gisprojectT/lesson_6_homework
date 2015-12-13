from helpers.base_component import BaseComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginForm(BaseComponent):
    selectors = {
        'self': 'login-form',
        'email_input': 'text-input-input',
        'password_input': 'password-input',
        'submit_button': 'login-button',
        'error_message': 'error-message'
    }

    def get_page_elem(self, selector):
        return self.driver.find_element_by_class_name(selector)

    def wait_page_elem(self, selector):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, selector)))

    def get_error_text(self):
        return self.driver.find_element_by_class_name(self.selectors["error_message"]).text

    def input_email(self, email):
        self.wait_page_elem(self.selectors["email_input"]).send_keys(email)

    def input_pass(self, password):
        self.get_page_elem(self.selectors["password_input"]).send_keys(password)

    def submit_sing_in(self):
        self.get_page_elem(self.selectors["submit_button"]).click()

    def wait_and_click_sing_in_button(self):
        self.wait_page_elem(self.selectors["submit_button"]).click()
