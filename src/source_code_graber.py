from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautogui import click as pag_click
from keyboard import press_and_release
from subprocess import Popen, PIPE
from os import getcwd, system, listdir, walk
from os.path import join
from time import sleep
from pyperclip import copy, paste
from time import time

system('cls')
username = ''
password = ''


def auto_get_source_code(username, password):
    url = 'https://itouch.cycu.edu.tw/home/'
    supported_chrome_version = ['104.0.5112', '105.0.5195', '106.0.5249']

    # system('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version')

    process = Popen(
        'reg query \"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon\" /v version', stdout=PIPE)
    version_info = process.stdout.readlines()
    version_info = str(version_info[2])
    version_info = version_info.lstrip(
        'b\'    version    REG_SZ    ').rstrip('\\r\\n\'')[:-4]
    driver_path = ''
    # print(version_info)
    if version_info in supported_chrome_version:
        index = supported_chrome_version.index(version_info)
        print(index)
        for root, dirs, files in walk(getcwd()):
            for file in files:
                if version_info in file:
                    print('found chromedriver')
                    driver_path = join(
                        root, file).replace('\\', '/')
                    print(driver_path)
                else:
                    print('chromedriver not found')
        if driver_path == '':
            print('chromedriver not found')
            return 'chromedriver not found'
    else:
        print('Unsupported Chrome Version')
        exit()
    # print(driver_path)

    driver = wd.Chrome(driver_path)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(20)

    try:
        username_input = driver.find_element(By.NAME, 'UserNm')
        username_input.send_keys(username)
        # username_input.submit()
        password_input = driver.find_element(By.NAME, 'UserPasswd')
        password_input.send_keys(password)
        password_input.submit()
        print('login success')
    except:
        pass

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')
        return 'login failed, please check your username and password or copy the source code manually'
    except:
        pass

    while True:
        try:
            sign_out = driver.find_element(
                By.XPATH, '//*[@id="left-PerfectScrollbar"]/div[1]/div/div/div[1]/div[2]/a')
            print('proved login success')
            break
        except:
            print('login failed')
            return 'login failed, please check your username and password or copy the source code manually'

    study = driver.find_element(
        By.XPATH, '//*[@id="left-PerfectScrollbar"]/div[3]/ul/li[3]')
    study.click()
    study_path = driver.find_element(
        By.XPATH, '//*[@id="left-PerfectScrollbar"]/div[3]/ul/li[4]/ul/li[4]')
    study_path.click()
    score_each_year = driver.find_element(
        By.XPATH, '//*[@id="left-PerfectScrollbar"]/div[3]/ul/li[4]/ul/li[5]/ul/li[3]/a[1]')
    score_each_year.click()
    while True:
        try:
            score_each_year = driver.find_element(
                By.XPATH, '//*[@id="container"]/div[1]/div[1]')
            score_each_year.click()
            print('proved score_each_year success')
            break
        except:
            print('score_each_year failed')
            pass
    pag_click(1816, 230)
    # bugged
    # open_in_new_window = driver.find_element(
    # By.LINK_TEXT, '/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/a[1]')
    # open_in_new_window.click()
    driver.switch_to.window(driver.window_handles[1])
    wait = 0.01  # sec
    soup = ''
    while '<html>' not in soup:
        wait = wait * 2
        sleep(wait)
        press_and_release('ctrl+u')
        sleep(wait)
        press_and_release('ctrl+a')
        sleep(wait)
        press_and_release('ctrl+c')
        sleep(wait)
        soup = paste()
        print('Successful copied.') if '<html>' in soup else print(
            'Falied to copy.')
    driver.quit()
    return soup


if __name__ == '__main__':
    print('This is a module, not a script.')
    soup = auto_get_source_code(username, password)
    # print(soup)
