#!./venv/bin/python
import unittest
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import subprocess

# from test_another import ScanQRCodeExample


lamassu_path = "/home/elliot/Documents/Projects/lamassu/lamassu-machine/"
mockPair = "SpYIG++FT5MRbZCzG2FBxFQvBZamIU4BOaWU38x8XQAbuIc9RwKtLjvVzNKb0J9157dsGqewk9fKZf/6/WKb8TEwNC4xMzEuNjcuMTI0"
mockBTC = "1KAkLnhU1BpvgjQUgLk1HF4PEgh4asFNS8"

active_section = "//section[@style='display: block;']"


class Example(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log_file = open('test-{:.0f}.log'.format(time.time()), 'wb')
        cls.p1 = subprocess.Popen(['ruby', lamassu_path + 'fake_id003.rb'], stdout=subprocess.PIPE)
        dev_name = cls.p1.stdout.readline().decode('ascii').strip()
        cls.p2 = subprocess.Popen(['node', lamassu_path + 'bin/lamassu-machine', '--mockCam', '--mockBillDispenser', '--mockBTC', mockBTC, '--mockBv', dev_name, '--mockPair', mockPair], stdout=cls.log_file, stderr=cls.log_file)
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    def test_insert_bill(self):
        driver = self.driver
        driver.get("file://" + lamassu_path + "ui/start.html")
        time.sleep(5)
        elem = driver.find_element_by_xpath(active_section)
        assert elem.is_displayed()

        elem.find_element_by_xpath(".//div[@class='circle-button']").click()

        time.sleep(5)

        elem = driver.find_element_by_xpath(active_section)

        sub_elem_title = elem.find_element_by_tag_name("h1").text
        self.assertEqual("Insert a bill", sub_elem_title)

    def test_scan_qr(self):
        driver = self.driver
        # driver.get("file://" + lamassu_path + "ui/start.html")
        driver.find_element_by_xpath(active_section).find_element_by_class_name("cancel").click()
        time.sleep(5)
        elem = driver.find_element_by_xpath(active_section)
        assert elem.is_displayed()

        elem.find_element_by_xpath(".//div[@class='circle-button']").click()

        time.sleep(0.5)

        elem = driver.find_element_by_xpath(active_section)
        self.assertEqual("scan-address", elem.get_attribute("data-tr-section"))

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.p1.terminate()
        cls.p2.terminate()
        cls.log_file.close()


if __name__ == "__main__":
    unittest.main()
