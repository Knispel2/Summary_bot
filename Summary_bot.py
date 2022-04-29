from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
import pickle
import pandas
import collections

def timesleep(sleeptime=1.7):
    time.sleep(sleeptime)

def example(f):
  try:
    return pickle.load(f)
  except EOFError:
    return set()



folder_path = r'C:\\FSR_Data' + '\\' + 'base' + '\\' + 'humans'
with open(folder_path, 'wb+') as f:
     seen = example(f)



folder_path = r'C:\FSR_Data' + '\\'

def give_chrome_option(folder_path):
    chromeOptions = webdriver.ChromeOptions() #setup chrome option
    prefs = {"download.default_directory" : folder_path,
           "download.prompt_for_download": False,
           "download.directory_upgrade": True}  #set path
    chromeOptions.add_experimental_option("prefs", prefs) #set option
    return chromeOptions
driver= webdriver.Chrome(ChromeDriverManager().install(), chrome_options = give_chrome_option(folder_path))
folder_path = 'C://FSR_Data/'

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
    pas.send_keys('86296953')
    timesleep()
    ok=vds.find_element_by_name('pageLogin_login_emp')
    ok.click()
except common.exceptions.NoSuchElementException:
    print('Already authtorised')
timesleep()



lnk=driver.find_element_by_link_text('Все заявления')
lnk.click()
ind=2
timesleep()
directions = []
try:
    while True:
        try:
            tbd=driver.find_element_by_tag_name('tbody')
            trs=tbd.find_elements_by_tag_name('tr')
            for i in trs:
                tds=i.find_elements_by_tag_name('td')
                num=tds[0].text.split('\n')[0]
                name=tds[1].text
                directions = directions + tds[3].text.split('\n')
                if num+name not in seen:
                    nname=name.split()
                    fname=nname[0]+'_'+nname[1][0]+(nname[2][0] if len(nname)>2 else '')+'_'+num
                    fname1=nname[0]+'_'+nname[1][0]+'_'+tds[0].text
                    fname2=nname[0]+'_'+nname[1][0]+'_'+num
                    #print(name,end=' ')
                    #print(fname1)
                    fname=fname.strip().casefold()
                    fname1=fname1.strip().casefold()
                    fname2=fname2.strip().casefold()
                    pdf_doc = folder_path + fname + '.pdf'
                    pdf_doc1 = folder_path + fname1 + '.pdf'
                    pdf_doc2 = folder_path + fname2 + '.pdf'
                    if (os.path.exists(pdf_doc) or (os.path.exists(pdf_doc1)) or (os.path.exists(pdf_doc2))):
                        seen.add(num+name)
                        continue
                    wa_doc = folder_path + fname + '.pdf'
                    wa_doc1 = folder_path + fname1 + '.pdf'
                    btn=tds[7].find_element_by_tag_name('button')
                    btn.click()
                    timesleep()
                    prt=driver.find_element_by_link_text('Печать')
                    prt.click()
                    timesleep()
                    mft=driver.find_element_by_class_name('modal-footer')
                    prt=mft.find_element_by_class_name('btn-primary')
                    prt.click()
                    tick=0
                    while not(os.path.exists(pdf_doc)):
                        if os.path.exists(pdf_doc1):
                            fname=fname1
                            pdf_doc=pdf_doc1
                            break
                        time.sleep(2)
                        tick+=1
                        if tick==10:
                            for file in filter(lambda x:x.endswith('.pdf'),os.listdir(folder_path)):
                                if nname[0].lower() in file:
                                    fname=file[:-4]
                                    pdf_doc=folder_path+fname+'.pdf'
                                    break
                            tick=0
                    seen.add(num+name)
        except Exception as err:
            print('*',err,'*')
            continue
        try:
            lnk=driver.find_element_by_link_text(str(ind))
            lnk.click()
        except:
            print("Страницы закончились")
            break
        timesleep()
        ind+=1
except (common.exceptions.ElementClickInterceptedException,common.exceptions.NoSuchElementException,common.exceptions.ElementNotInteractableException) as err:
    print(err)



print(collections.Counter(directions))
print()

with open(r'C:\\FSR_Data' + '\\' + 'base' + '\\' + 'humans','wb') as f: 
    pickle.dump(seen,f) #тут надо как-то переделать