class LoginForm:
    def __init__(self, driver):
        self.driver = driver
        self._form = None

    @property
    def form(self):
        from helpers.pages.LoginForm.login_form import LoginForm

        if self._form is None:
            self._form = LoginForm(self.driver, self.driver.find_element_by_class_name(
                LoginForm.selectors["self"]))
        return self._form
