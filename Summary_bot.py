from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
import pandas
import collections
import fitz
from datetime import datetime

def timesleep(sleeptime=1.7):
    time.sleep(sleeptime)

def example():
  try:
      return pandas.read_csv(folder_path + 'base.csv')
  except:
      return pandas.DataFrame(columns = ['ID', 'ФИО', 'Дата', 'Номер телефона', 'Полис', 'Статус согласия', 'Статус ошибок', 'Вместо ЕГЭ'])

def PDFtoINFO(file):
    try:
        folder='C:/FSR_Data/'
        data = [None]*3
        doc=fitz.open(file) #кряк с директорией
        base = str(doc.loadPage(2).getText())
        print(base)
        if 'Фундаментальная математика и механика' in doc.loadPage(0).getText():
            if '''Основания для участия в конкурсе по результатам вступительных испытаний, проводимых МГУ для отдельных
        категорий поступающих (вместо ЕГЭ)
        0''' in doc.loadPage(0).getText():
                data[0] = 0
            else:
                data[0] = 1
            j = base.find('КОНТАКТНЫЕ ТЕЛЕФОНЫ (городской с кодом города и мобильный) И АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ')
            start = 2 + j + len('КОНТАКТНЫЕ ТЕЛЕФОНЫ (городской с кодом города и мобильный) И АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ')
            buf = []
            while(base[start] != '.'):
                if base[start] not in {'\n', ' '}:
                    buf.append(base[start])
                start+=1
                if base[start] == '.':
                    buf.append(base[start])
                    buf.append(base[start+1])
                    buf.append(base[start+2])
            data[1] = ''.join(buf) 
            j = base.find('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
        (при наличии)''')
            start = 1 + j + len('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
        (при наличии)''')
            buf = []
            while(base[start] != 'С'):
                if base[start] not in {'\n', ' '}:
                    buf.append(base[start])
                start+=1
            data[2] = ''.join(buf)
        else:
            base = str(doc.loadPage(1).getText())
            j = base.find('КОНТАКТНЫЕ ТЕЛЕФОНЫ (городской с кодом города и мобильный) И АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ')
            start = 2 + j + len('КОНТАКТНЫЕ ТЕЛЕФОНЫ (городской с кодом города и мобильный) И АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ')
            buf = []
            indicator = '@'
            while(base[start] != indicator):
                if base[start] not in {'\n', ' '}:
                    buf.append(base[start])
                start+=1
                if base[start] == '@':
                    indicator = '.'
            data[1] = ''.join(buf) 
            j = base.find('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
        (при наличии)''')
            start = 1 + j + len('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
        (при наличии)''')
            buf = []
            while(base[start] != 'С'):
                if base[start] not in {'\n', ' '}:
                    buf.append(base[start])
                start+=1
            data[2] = ''.join(buf)
    except:
        print('*',err,'*')
        input()
    return data


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
ind=2
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

                if main_base['ID'].astype(str).str.contains(num).any():
                    try:
                        buffer = str(main_base[main_base['ID'] == int(num)]['Дата'].astype(str)).split('    ')[1].strip('\n')
                    except:
                        print(str(main_base[main_base['ID'] == int(num)]['Дата'].astype(str)))
                    if (to_realtime(buffer) == to_realtime(str(data_time))):
                        continue
                    else:
                        os.remove(pdf_doc)
                        os.remove(pdf_doc1)
                        os.remove(pdf_doc2)
                        main_base.loc[df['ID'] == num, 'Дата'] = data_time
                        main_base.loc[df['ID'] == num, 'Статус ошибок'] = status                
                        
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
                flag = True
                if os.path.exists(pdf_doc):
                    PDFinfo = PDFtoINFO(pdf_doc)
                elif os.path.exists(pdf_doc1):
                    flag = False
                    PDFinfo = PDFtoINFO(pdf_doc1)

                new_row = {'ID':num, 'ФИО':name, 'Дата' : data_time, 'Номер телефона': PDFinfo[1], 'Полис' : PDFinfo[2],
                           'Статус согласия': '-', 'Статус ошибок' : status, 'Вместо ЕГЭ' : PDFinfo[0]}                
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


