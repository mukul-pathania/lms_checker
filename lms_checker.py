from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import time
import sys


def login(browser):
    browser.get('http://mydy.dypatil.edu')
    username = input('Enter your username: ')
    password = getpass.getpass()
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('loginbtn').click()
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('loginbtn').click()
    if browser.title != 'Dashboard':
        print('Incorrect username or password provided.')
        sys.exit()


def chooseSubject(browser):
    print('Which subject do you wish to complete?\n\n1.POC\n2.DBMS\n3.DSA\n4.Maths\n5.PCPF\n6.Exit')
    while True:
        choice = int(input('Enter your choice: '))
        if 1 <= choice <= 5:
            return choice
        elif choice == 6:
            try:
                browser.quit()
                sys.exit()
            except:
                sys.exit()
        else:
            choice = int(
                input('Invalid choice!!\n Choose one of the given options: '))


def openSubject(browser):
    choice = chooseSubject(browser)
    if 1 <= choice <= 4:
        browser.find_elements_by_class_name('launchbutton')[choice - 1].click()

    elif choice == 5:
        browser.find_element_by_link_text('Next').click()
        browser.find_element_by_class_name('launchbutton').click()

    # time.sleep(5)


def browseUncompleted(browser):
    try:
        isPercentElementLoaded = EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.content span'))
        WebDriverWait(browser, 10).until(isPercentElementLoaded)
    except TimeoutException:
        print('Timed out waiting for the percentage element to load')
    finally:
        browser.find_element_by_css_selector('.content span').click()

    # Check if anything is pending and work accordingly
    try:
        # it is elements here not element be careful
        links = browser.find_elements_by_css_selector('a.pending')
    except Exception as e:
        print(e)
        # if no element is found then it means that everything is completed already
        return

    previous_length = len(links)
    j = -1
    for i in range(len(links)):
        # storing links in a variable directly won't work as page is being refreshed many times
        print('Working on link number ', i)
        try:
            isPageLoaded = EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a.pending'))
            WebDriverWait(browser, 10).until(isPageLoaded)
        except TimeoutException:
            print('Timed out waiting for page to load')
        finally:
            pending_links = browser.find_elements_by_css_selector('a.pending')
            if not len(pending_links) < previous_length:
                j += 1
            pending_links[j].click()
            browser.back()
            previous_length = len(pending_links)
            # time.sleep(3)


def logout(browser):
    browser.find_element_by_css_selector('.usermenu').click()
    browser.find_element_by_link_text('Log out').click()


def run():
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()
    login(browser)
    openSubject(browser)
    windows = browser.window_handles
    browser.switch_to.window(windows[1])
    print(browser.title)
    # return browser
    browseUncompleted(browser)
    browser.close()
    browser.switch_to.window(windows[0])
    logout(browser)
    # browser.quit()
    print('Work completed')
    print('Are you logged out?')


if __name__ == '__main__':
    run()
