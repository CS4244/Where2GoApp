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
def killPhantomJs():
    os.system('taskkill /f /im phantomjs.exe')
    os.system('taskkill /f /im Xvfb.exe')

def getBeginField(driver):
    return driver.find_element_by_css_selector('#beginBtn')


def clickBeginField(driver):
    getBeginField(driver).click()


def isNextFieldPresent(driver):
    try:
        isPresent = driver.find_element_by_css_selector('#nextBtn')
    except:
        driver.save_screenshot(os.getcwd()+'\\'+str(time.time())+'.png')
        killPhantomJs()
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
    display = Display(visible=0, size=(800, 600))
    display.start()
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
            numToCheck = random.randrange(1, len(elem) + 1)#decide how many to check
            print("Actual Length = ", len(elem), "  To check = ", numToCheck)
            actualCheckBoxNumber = []#to store which box to actually check
            while numToCheck > 0:
                randNum = random.randrange(0, len(elem))
                if randNum not in actualCheckBoxNumber:
                    actualCheckBoxNumber.append(randNum)
                    numToCheck -= 1
            for i in actualCheckBoxNumber:
                elem[i].click()
        except:
            pass
        clickNextField(driver)
    # print(os.getcwd())



if __name__ == '__main__':
    main()
