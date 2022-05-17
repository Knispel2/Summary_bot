from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
import pandas
import collections
import fitz
from datetime import datetime
from PDFtoINFO import PDFtoINFO_brute

def timesleep(sleeptime=1.7):
    time.sleep(sleeptime)

def example():
  try:
      return pandas.read_csv(folder_path + 'base.csv')
  except:
      return pandas.DataFrame(columns = ['ID', 'ФИО', 'Дата', 'Номер телефона', 'Полис', 'Статус согласия', 'Статус ошибок', 'Вместо ЕГЭ', 'Направление'])


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


def to_realtime(data):
    dateFormatter = "%d.%m.%Y %H:%M:%S"
    data = str(data).split('\n')[0]
    return datetime.strptime(data, dateFormatter)

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
ind=27
timesleep()
directions = []
try:
    while True:
        try:
            tbd=driver.find_element_by_tag_name('tbody')
            trs=tbd.find_elements_by_tag_name('tr') #множество строк
            for i in trs:
                folder_path = r'C:\\FSR_Data' + '\\' + 'base' + '\\'
                main_base =  example()
                folder_path = r'C:\FSR_Data' + '\\'

                tds=i.find_elements_by_tag_name('td') #отдельно взятая строка
                if 'С' in tds[0].text:
                    sogl = True
                else:
                    sogl = False
                num=tds[0].text.split('\n')[0]
                name=tds[1].text
                data_time = tds[6].text
                status = tds[5].text
                direction = tds[3].text.split('\n')
                directions = directions + tds[3].text.split('\n')
                
                nname=name.split()
                fname=nname[0]+'_'+nname[1][0]+(nname[2][0] if len(nname)>2 else '')+'_'+num
                fname1=nname[0]+'_'+nname[1][0]+'_'+tds[0].text
                fname2=nname[0]+'_'+nname[1][0]+'_'+num
                fname=fname.strip().casefold()
                fname1=fname1.strip().casefold()
                fname2=fname2.strip().casefold()
                pdf_doc = folder_path + fname + '.pdf'
                pdf_doc1 = folder_path + fname1 + '.pdf'
                pdf_doc2 = folder_path + fname2 + '.pdf'

                if main_base['ID'].astype(str).str.contains(num).any(): #а вот тут надо использовать другой способ для отслеживания
                    #здесь надо сделать обработку согласия
                    debug_data3 = str(main_base[main_base['ID'] == int(num)]['ФИО'].astype(str))
                    try:
                        buffer = str(main_base[main_base['ID'] == int(num)]['Дата'].astype(str)).split('    ')[1].strip('\n')
                    except:
                        print(str(main_base[main_base['ID'] == int(num)]['Дата'].astype(str)))
                    if (to_realtime(buffer) == to_realtime(str(data_time))):
                        continue
                    else:
                        try:
                            os.remove(pdf_doc)
                            main_base.loc[main_base['ID'] == num, 'Дата'] = data_time
                            main_base.loc[main_base['ID'] == num, 'Статус ошибок'] = status
                        except:
                            try:
                                os.remove(pdf_doc1)
                                main_base.loc[main_base['ID'] == num, 'Дата'] = data_time
                                main_base.loc[main_base['ID'] == num, 'Статус ошибок'] = status
                            except:
                                try:
                                   os.remove(pdf_doc2)
                                   main_base.loc[main_base['ID'] == num, 'Дата'] = data_time
                                   main_base.loc[main_base['ID'] == num, 'Статус ошибок'] = status
                                except:
                                    print("Не удалось удалить")
                                    
                                        
                        
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
                while not(os.path.exists(pdf_doc)) or not(os.path.exists(pdf_doc2)):
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
                flag = True
                if os.path.exists(pdf_doc):
                    PDFinfo = PDFtoINFO_brute(pdf_doc)
                elif os.path.exists(pdf_doc1):
                    flag = False
                    PDFinfo = PDFtoINFO_brute(pdf_doc1)
                elif os.path.exists(pdf_doc1):
                    flag = False
                    PDFinfo = PDFtoINFO_brute(pdf_doc1)
                new_row = {'ID':num, 'ФИО':name, 'Дата' : data_time, 'Номер телефона': PDFinfo[1], 'Полис' : PDFinfo[2],
                           'Статус согласия': sogl, 'Статус ошибок' : status, 'Вместо ЕГЭ' : PDFinfo[0], 'Направление' : direction}                
                main_base = main_base.append(new_row, ignore_index=True)
                folder_path = r'C:\\FSR_Data' + '\\' + 'base' + '\\'
                main_base.to_csv(folder_path + 'base.csv', index=False)
                folder_path = 'C://FSR_Data/'
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


