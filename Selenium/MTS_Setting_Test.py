# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class MTSSettingTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://cscr-mts.cscr.hp.com:9080"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_m_t_s_setting(self):
        driver = self.driver
        driver.get(self.base_url + "/index.html")
        time.sleep(5)
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_id("emails").clear()
        driver.find_element_by_id("emails").send_keys("song.qi@hp.com")
        driver.find_element_by_id("passwords").clear()
        driver.find_element_by_id("passwords").send_keys("Ricky")
        driver.find_element_by_css_selector("input[type=\"button\"]").click()
        time.sleep(5)
        driver.find_element_by_link_text("Settings").click()
        driver.find_element_by_css_selector("b").click()
        driver.find_element_by_id("ipAddress").clear()
        driver.find_element_by_id("ipAddress").send_keys("15.74.177.49")
        driver.find_element_by_id("ipPort").clear()
        driver.find_element_by_id("ipPort").send_keys("9070")
        driver.find_element_by_id("location").clear()
        driver.find_element_by_id("location").send_keys("WX_")
        driver.find_element_by_id("location").clear()
        driver.find_element_by_id("location").send_keys("WX_MacMini01")
        driver.find_element_by_id("getDeviceDetailsid").click()
        time.sleep(5)
        select = Select(driver.find_element_by_id("mobile"))
        select.select_by_visible_text("iPad 2 (9.0 )")
        select = Select(driver.find_element_by_id("mobile"))
        select.select_by_visible_text("iPad 2 (9.3 )")
        select = Select(driver.find_element_by_id("mobile"))
        select.select_by_visible_text("iPad Air (9.0 )")
        select = Select(driver.find_element_by_id("mobile"))
        select.select_by_visible_text("iPad Air (9.3 )")
        select = Select(driver.find_element_by_id("mobile"))
        select.select_by_visible_text("iPhone 6 (9.3 )")
        select = Select(driver.find_element_by_id("android"))
        select.select_by_visible_text("GoogleNexus6P")
        select = Select(driver.find_element_by_id("android"))
        select.select_by_visible_text("GoogleNexus4")
        select = Select(driver.find_element_by_id("android"))
        select.select_by_visible_text("MotorolaMotoX")
        select = Select(driver.find_element_by_id("frameWorks"))
        select.select_by_visible_text("Appium")
        select = Select(driver.find_element_by_id("frameWorks"))
        select.select_by_visible_text("Python")
        driver.find_element_by_xpath("//input[@id='edit']").click()
        time.sleep(5)
    
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
