# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementExceptions
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.firefox_bianry import FirefoxBianrys
import unittest, time, re

class Test(unittest.TestCase):
    def setUp(self):
        binary = FirefoxBinary(r"D:\Firefox\firefox.exe")
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://jimmylee05.github.io/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Read More").click()
        driver.find_element_by_link_text("Archives").click()
        driver.find_element_by_link_text("Tags").click()
        driver.find_element_by_css_selector("i.logo").click()
        driver.find_element_by_css_selector("img.article-banner").click()
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_css_selector("#post-hello-world > div.article-inner > a > img.article-banner").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
