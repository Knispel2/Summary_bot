from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
seen=set()
driver=webdriver.Chrome(ChromeDriverManager().install())

def timesleep(sleeptime=1.7):
    time.sleep(sleeptime)

url='https://webanketa.msu.ru/index.php#panel-login-internal'
driver.get(url)
try:
    lnk=driver.find_element_by_link_text('Вход для сотрудников')
    lnk.click()
    timesleep()
    vds=driver.find_element_by_id('panel-login-internal')
    login=vds.find_element_by_id('pageLogin_login')
    login.send_keys('39_vladikina.v.e.')
    pas=vds.find_element_by_name('pageLogin_password')
    pas.send_keys('77152213')
    timesleep()
    ok=vds.find_element_by_name('pageLogin_login_emp')
    ok.click()
except common.exceptions.NoSuchElementException:
    print('Already authtorised')
timesleep()