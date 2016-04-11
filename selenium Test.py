import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import time
import random, time, sys

__author__ = 'GARY WONG'




########################################################################################################
def getBeginField(driver):
    return driver.find_element_by_css_selector('#beginBtn')


def clickBeginField(driver):
    getBeginField(driver).click()


def isNextFieldPresent(driver):
    try:
        isPresent = driver.find_element_by_css_selector('#nextBtn')
    except:
        # driver.save_screenshot(os.getcwd()+'\\test1.png')
        driver.close()
        driver.quit()
        sys.exit()


    return isPresent


def clickNextField(driver):
    isNextFieldPresent(driver).click()


def clickTextBox(driver):
    isTextBoxPresent(driver).click()


def isTextBoxPresent(driver):
    try:
        isPresent = driver.find_element_by_css_selector('#textbox')
    except:
        return False
    return isPresent


def clickRadio(driver):
    isRadioPresent(driver).click()


def isRadioPresent(driver):
    try:
        isPresent = driver.find_element_by_css_selector('#radio')
    except:
        return False
    return isPresent


def clickCheckBox(driver):
    isCheckBoxPresent(driver).click()


def isCheckBoxPresent(driver):
    try:
        isPresent = driver.find_element_by_css_selector('#checkbox')
    except:
        return False
    return isPresent


########################################################################################################
def main():
    dCap = dict(DesiredCapabilities.PHANTOMJS)
    dCap['phantomjs.page.settings.useragent'] = (
    'mozilla/5.0 (windows nt 6.3; wow64) applewebkit/537.36 (khtml, like gecko) chrome/43.0.2357.81 safari/537.36')
    driver = webdriver.PhantomJS(executable_path="d:\install location\phantomjs\\bin\phantomjs.exe",
                                 desired_capabilities=dCap)
    # driver = webdriver.Firefox()

    driver.get("http://localhost:5000/expertapp/")
    clickBeginField(driver)
    clickTextBox(driver)

    elem = driver.find_element_by_name("budget")
    if elem:
        elem.send_keys(random.randrange(0, 1000, 50))
    clickNextField(driver)

    elem = driver.find_element_by_name("daysReq")
    if elem:
        elem.send_keys(random.randrange(0, 10, 1))
    clickNextField(driver)

    while True:
        try:
            elem = driver.find_elements_by_css_selector("#radio")
            elem[random.randrange(0, len(elem))].click()
        except:
            pass
        try:
            elem = driver.find_elements_by_css_selector("#checkbox")
            numToCheck = random.randrange(1, len(elem) + 1)
            print("Actual Length = ", len(elem), "  To check = ", numToCheck)
            for i in range(0, numToCheck):
                elem[i].click()
        except:
            pass
        clickNextField(driver)
    # print(os.getcwd())



if __name__ == '__main__':
    main()
