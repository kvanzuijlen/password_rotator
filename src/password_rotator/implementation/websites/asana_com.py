import re

from selenium.webdriver.common.by import By

from password_rotator.implementation import SeleniumBase


class AsanaCom(SeleniumBase):
    @classmethod
    def website(cls) -> str:
        return "asana.com"

    @classmethod
    def is_valid_for(cls, domain: str) -> bool:
        return re.compile(r"^(.+\.)*asana.com$").match(domain) is not None

    def _change_password(self):
        self.driver.get("https://asana.com")
        self.driver.find_element(By.LINK_TEXT, "Inloggen").click()
        self.driver.find_element(By.ID, "lui_16").send_keys(self._password_entry.username)
        self.driver.find_element(By.CSS_SELECTOR, ".ThemeableRectangularButtonPresentation--large").click()
        self.driver.find_element(By.ID, "lui_3").send_keys(self._password_entry.secret)
        self.driver.find_element(By.CSS_SELECTOR, ".ThemeableRectangularButtonPresentation--isEnabled").click()
        self.driver.find_element(By.CSS_SELECTOR, ".TopbarPageHeaderGlobalActions-settingsMenuAvatar").click()
        self.driver.find_element(By.CSS_SELECTOR, ".ThemeableItemBackgroundStructure--isHighlighted").click()
        self.driver.find_element(By.CSS_SELECTOR, ".TabNavigationBarItem:nth-child(4) .TabNavigationBarItem-selectableTab--isClickable").click()
        self.driver.find_element(By.CSS_SELECTOR, ".ProfileSettingsDialogPasswordForm-rowLink").click()
        self.driver.find_element(By.CSS_SELECTOR, ".FormRowStructure--labelPlacementTop:nth-child(1) .TextInputBase").click()
        self.driver.find_element(By.CSS_SELECTOR, ".FormRowStructure--labelPlacementTop:nth-child(1) .TextInputBase").send_keys(self._password_entry.secret)
        self.driver.find_element(By.CSS_SELECTOR, ".FormRowStructure--labelPlacementTop:nth-child(2) .TextInputBase").click()
        self.driver.find_element(By.CSS_SELECTOR, ".FormRowStructure--labelPlacementTop:nth-child(3) .TextInputBase").send_keys(self._new_password)
        self.driver.find_element(By.CSS_SELECTOR, ".FormRowStructure--labelPlacementTop:nth-child(2) .TextInputBase").send_keys(self._new_password)
        self.driver.find_element(By.CSS_SELECTOR, ".ProfileSettingsDialogPasswordForm-button:nth-child(2)").click()
