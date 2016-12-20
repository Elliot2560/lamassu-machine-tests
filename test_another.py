#!./venv/bin/python
import unittest
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import subprocess


lamassu_path = "/home/elliot/Documents/Projects/lamassu/lamassu-machine/"
mockPair = "SpYIG++FT5MRbZCzG2FBxFQvBZamIU4BOaWU38x8XQAbuIc9RwKtLjvVzNKb0J9157dsGqewk9fKZf/6/WKb8TEwNC4xMzEuNjcuMTI0"
mockBTC = "1KAkLnhU1BpvgjQUgLk1HF4PEgh4asFNS8"

active_section = "//section[@style='display: block;']"


class ScanQRCodeExample(unittest.TestCase):

    def setUp(self):
        self.log_file = open('test-{:.0f}.log'.format(time.time()), 'wb')
        self.p1 = subprocess.Popen(['ruby', lamassu_path + 'fake_id003.rb'], stdout=subprocess.PIPE)
        dev_name = self.p1.stdout.readline().decode('ascii').strip()
        self.p2 = subprocess.Popen(['node', lamassu_path + 'bin/lamassu-machine', '--mockCam', '--mockBillDispenser', '--mockBTC', mockBTC, '--mockBv', dev_name, '--mockPair', mockPair], stdout=self.log_file, stderr=self.log_file)
        self.driver = webdriver.Chrome()

    def test_insert_bill(self):
        driver = self.driver
        driver.get("file://" + lamassu_path + "ui/start.html")
        # driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(5)
        elem = driver.find_element_by_xpath(active_section)
        assert elem.is_displayed()

        elem.find_element_by_xpath(".//div[@class='circle-button']").click()

        time.sleep(0.5)

        elem = driver.find_element_by_xpath(active_section)
        self.assertEqual("scan-address", elem.get_attribute("data-tr-section"))

    def tearDown(self):
        self.driver.close()
        self.p1.terminate()
        self.p2.terminate()
        self.log_file.close()
