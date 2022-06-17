from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
import pandas
import collections
import fitz
import numpy
from datetime import datetime
from PDFtoINFO import PDFtoINFO_brute


#####################################################
#Некоторые служебные и инициализирующие функции, перечень известных олимпиадников
######################################################
def timesleep(sleeptime=1.7):
    time.sleep(sleeptime)

def example(folder_path):
  try:
      return pandas.read_csv(folder_path + 'base.csv')
  except:
      return pandas.DataFrame(columns = ['ID', 'ФИО', 'Дата', 'Номер телефона', 'Полис', 'Статус согласия', 'Статус ошибок', 'Вместо ЕГЭ', 'Направление', 'Зона', 'Новое согласие?', 'Олимпиадник?'])


def give_chrome_option(folder_path):
    chromeOptions = webdriver.ChromeOptions() #setup chrome option
    prefs = {"download.default_directory" : folder_path,
           "download.prompt_for_download": False,
           "download.directory_upgrade": True}  #set path
    chromeOptions.add_experimental_option("prefs", prefs) #set option
    return chromeOptions



def to_realtime(data):
    dateFormatter = "%d.%m.%Y %H:%M:%S"
    data = str(data).split('\n')[0]
    return datetime.strptime(data.strip(), dateFormatter)

kosm_pobedpriz='''ГАЙДУКОВ АЛЕКСАНДР ЕВГЕНЬЕВИЧ
ТЕЛЕЛЮХИН КОНСТАНТИН СЕРГЕЕВИЧ
ВЕНГЕРСКАЯ АННА СЕРГЕЕВНА
КУДРЯВЦЕВ АНДРЕЙ ДМИТРИЕВИЧ
МОСАЛЕВ МАКСИМ СЕРГЕЕВИЧ
ЦЫПОЧКА ДАНИИЛ ГРИГОРЬЕВИЧ
ЩЕРБАКОВ НИКИТА ДЕНИСОВИЧ'''.split('\n')

vseross='''АЛЁШИН АНДРЕЙ СЕРГЕЕВИЧ
ЖИВИН АЛЕКСЕЙ ИВАНОВИЧ
ИГНАТЬЕВ ИВАН ВЯЧЕСЛАВОВИЧ
МАСЛАКОВ ИВАН НИКОЛАЕВИЧ
МУРАТОВ ВАСИЛИЙ АНДРЕЕВИЧ
ПЕРМЯКОВ МАКСИМ ДМИТРИЕВИЧ
ПРОСЯНОЙ ИЛЬЯ СЕРГЕЕВИЧ
АЛЬ-ХАДЖ АЮБ САЛЕХ МУХАММЕД МАДИАНОВИЧ
БЕСПЯТЫЙ ИЛЬЯ ВИТАЛЬЕВИЧ
БОБКОВА ЕКАТЕРИНА СЕРГЕЕВНА
ВЕЛИКАНОВ ПАВЕЛ АРТЕМОВИЧ
ВОЛОШИНОВ ВЛАДИМИР ВЛАДИСЛАВОВИЧ
ЖДАНОВ ЕЛИСЕЙ АЛЕКСЕЕВИЧ
ЗАБЕЛКИН МАКСИМ АНДРЕЕВИЧ
ИВАНОВ ДМИТРИЙ АНДРЕЕВИЧ
КАЛАШНИКОВ МИХАИЛ МАКСИМОВИЧ
КРАСОТКИНА ВИКТОРИЯ ВЯЧЕСЛАВОВНА
ЛАЗАРЕВ АНТОН ДЕНИСОВИЧ
ЛЫМАРЕВА ДАРЬЯ НИКОЛАЕВНА
МАКСИМОВА ЕЛИЗАВЕТА КОНСТАНТИНОВНА
МЕНТИЙ АРТЕМИЙ ПАВЛОВИЧ
МИНЕЕВ ИЛЬЯ МАКСИМОВИЧ
НЕФЕДОВ ИВАН ВЯЧЕСЛАВОВИЧ
ПАТЕШМАН ЕГОР АЛЕКСАНДРОВИЧ
ПЕЛИПЕНКО РОМАН АНДРЕЕВИЧ
ПЛУЖНИКОВА ВЕРОНИКА ВЛАДИСЛАВОВНА
ПОЛОНЧУК НИКОЛАЙ АНДРЕЕВИЧ
ПОНАМАРЕВ АЛЕКСЕЙ ВИТАЛЬЕВИЧ
РАМЕНСКИЙ МАКСИМ СЕРГЕЕВИЧ
РАЧКОВ МИХАИЛ ВАСИЛЬЕВИЧ
САФАРАЛИЕВ АЛАН ДАМИРОВИЧ
СЕВАСТЬЯНОВ КОНСТАНТИН КИРИЛЛОВИЧ
СТУРОВ ФЁДОР АЛЕКСЕЕВИЧ
ТУХВАТУЛИН ДАНИЯР ГАЗИМОВИЧ
ЧАПАЕВА ИРИНА ВЯЧЕСЛАВОВНА
ШАШКОВ ДАНИЛА АЛЕКСАНДРОВИЧ
ЩЕРБОНОС МАКСИМ БОРИСОВИЧ
ЮРИКОВ НИКИТА ИВАНОВИЧ
АНТОНОВ РУСЛАН ВИТАЛЬЕВИЧ
БАТУРИН ГЕРМАН ДЕНИСОВИЧ
БАШТА НИКИТА ДМИТРИЕВИЧ
БЕРНШТЕЙН ВАДИМ ЮРЬЕВИЧ
ГРИГОРЬЕВА АНАСТАСИЯ МИХАЙЛОВНА
ДУБОВИЦКИЙ МАКСИМ АРТЕМОВИЧ
ЕФИМОВ КИРИЛЛ ПЕТРОВИЧ
КОЗЫРЕВ МИХАИЛ АЛЕКСЕЕВИЧ
КОНОВАЛОВ АРТЕМ АНДРЕЕВИЧ
КОТЕЛЬНИКОВ ИВАН ВЛАДИМИРОВИЧ
КУЗНЕЦОВ ИВАН АЛЕКСАНДРОВИЧ
КУЗНЕЦОВ ИВАН СТАНИСЛАВОВИЧ
ЛЕВЧЕНКО БОГДАН АЛЕКСЕЕВИЧ
НИСТЮК АЛЕКСЕЙ АНАТОЛЬЕВИЧ
ПЯТКЕВИЧ ЭРИК ЯНОВИЧ
РАМЕНСКИЙ МАКСИМ СЕРГЕЕВИЧ
СОКОЛОВСКИЙ МАКСИМИЛИАН АНДРЕЕВИЧ
СТРЕБУЛАЕВ ВИКТОР СЕРГЕЕВИЧ
ТИМАКОВ АНДРЕЙ АЛЕКСЕЕВИЧ
ШАРЫПОВ ЮСУФ ЗАКИРОВИЧ
ЮДЕНИЧ АНАСТАСИЯ РОМАНОВНА
ЯРОШЕВИЧ МИХАИЛ ВАСИЛЕВИЧ'''.split('\n')
#####################################################
#####################################################






#####################################################
#Далее идёт основной код#############################

def Webanketa_update():
    folder_path = r'C:\FSR_Data' + '\\'
    driver= webdriver.Chrome(ChromeDriverManager().install(), chrome_options = give_chrome_option(folder_path))
    url='https://webanketa.msu.ru/index.php#panel-login-internal'
    driver.get(url)
    try:
        lnk=driver.find_element_by_link_text('вход для сотрудников')
        lnk.click()
        timesleep()
        login=driver.find_element_by_id('login_0_0_phone_phone')
        login.send_keys('9002538683')    
        pas=driver.find_element_by_name('login_password')
        pas.send_keys('2507570366')
        timesleep()
        vds=driver.find_element_by_class_name('login')
        vds.click()
    except common.exceptions.NoSuchElementException:
        print('Already authtorised')
        return 1
    timesleep()
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
                    main_base =  example(folder_path)
                    folder_path = r'C:\FSR_Data' + '\\'
                    tds=i.find_elements_by_tag_name('td') #отдельно взятая строка
                    BVI = "Нет"
                    if 'С' in tds[0].text:
                        try:
                            sogl = tds[0].find_element_by_class_name('btn-success').get_attribute('data-original-title')
                        except:
                            sogl = tds[0].find_element_by_class_name('btn-danger').get_attribute('data-original-title')
                    else:
                        sogl = "Нет"
                    num=tds[0].text.split('\n')[0].strip()
                    name=tds[1].text
                    data_time = tds[6].text
                    status = tds[5].text
                    direction = tds[3].text.split('\n')[0]
                    directions = directions + tds[3].text.split('\n')
                    update_flag = False
                    nname=name.split()
                    fname=nname[0]+'_'+nname[1][0]+(nname[2][0] if len(nname)>2 else '')+'_'+num
                    fname1=nname[0]+'_'+nname[1][0]+'_'+tds[0].text
                    fname2=nname[0]+'_'+nname[1][0]+'_'+num
                    fname_ultra = nname[0]+'_'+nname[1]+'_'+num
                    fname=fname.strip().upper()
                    fname1=fname1.strip().upper()
                    fname2=fname2.strip().upper()
                    fname_ultra=fname_ultra.strip().upper()
                    pdf_doc = folder_path + fname + '.pdf'
                    pdf_doc1 = folder_path + fname1 + '.pdf'
                    pdf_doc2 = folder_path + fname2 + '.pdf'
                    pdf_doc_ultra = folder_path + fname_ultra + '.pdf'
                    new_sogl_status = False
                    debug_delta = main_base['ID'].unique()
                    if numpy.int64(num) in debug_delta:
                        print(main_base.loc[main_base['ID'] == numpy.int64(num), 'Статус согласия'].unique()[0])
                        if (main_base.loc[main_base['ID'] == numpy.int64(num), 'Статус согласия'].unique()[0] != sogl):
                            new_sogl_status = True
                        main_base.loc[main_base['ID'] == numpy.int64(num), ['Статус согласия']] = sogl
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
                            except:
                                try:
                                    os.remove(pdf_doc1)
                                except:
                                    try:
                                       os.remove(pdf_doc_ultra)                                   
                                    except:
                                        print("Не удалось удалить")
                        try:
                            print(main_base.loc[main_base['ID'] == numpy.int64(num), ['Дата']])
                            main_base.loc[main_base['ID'] == numpy.int64(num), ['Дата']] = data_time
                            main_base.loc[main_base['ID'] == numpy.int64(num), ['Статус ошибок']] = status
                        except:
                            print("Кряк")
                        update_flag = True
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
                    while True:
                        if not(os.path.exists(pdf_doc)) and not(os.path.exists(pdf_doc2)) and not(os.path.exists(pdf_doc_ultra)):
                            continue
                        if os.path.exists(pdf_doc1):
                            fname=fname1
                            pdf_doc=pdf_doc1
                            break
                        if os.path.exists(pdf_doc2):
                            fname=fname1
                            pdf_doc=pdf_doc2
                            break
                        if os.path.exists(pdf_doc_ultra):
                            fname=fname_ultra
                            pdf_doc=pdf_doc_ultra
                            break
                        time.sleep(2)
                        #tick+=1
                        #if tick==10:
                        #    for file in filter(lambda x:x.endswith('.pdf'),os.listdir(folder_path)):
                        #        if nname[0].upper() in file:
                        #            fname=file[:-4]
                        #            pdf_doc=folder_path+fname+'.pdf'
                        #            break
                        #    tick=0
                    flag = True
                    if os.path.exists(pdf_doc):
                        PDFinfo = PDFtoINFO_brute(pdf_doc)
                    elif os.path.exists(pdf_doc1):
                        flag = False
                        PDFinfo = PDFtoINFO_brute(pdf_doc1)
                    elif os.path.exists(pdf_doc1):
                        flag = False
                        PDFinfo = PDFtoINFO_brute(pdf_doc1)
                    if name.upper() in kosm_pobedpriz:
                        BVI = "Победопризёр космонавтики"
                    elif name.upper() in vseross:
                        BVI = "Всероссник по астрономии"
                    new_row = {'ID':num, 'ФИО':name.upper(), 'Дата' : data_time, 'Номер телефона': PDFinfo[1], 'Полис' : PDFinfo[2],
                               'Статус согласия': sogl, 'Статус ошибок' : status, 'Вместо ЕГЭ' : PDFinfo[0], 'Направление' : direction, 'Зона' : PDFinfo[3], 'Новое согласие?' : new_sogl_status, 'Олимпиадник?' : BVI}                
                    if not update_flag:
                        main_base = main_base.append(new_row, ignore_index=True)
                    folder_path = r'C:\\FSR_Data' + '\\' + 'base' + '\\'
                    main_base.to_csv(folder_path + 'base.csv', index=False, encoding="utf-8")
                    folder_path = 'C://FSR_Data/'
            except Exception as err:
                print('*',err,'*')
                continue
            try:            
                lnk=driver.find_element_by_link_text(str(ind))
                lnk.click()
            except:
                try:
                    btn.click()
                    lnk=driver.find_element_by_link_text(str(ind))
                    lnk.click()
                except:
                    print("Страницы закончились:", str(ind))
                    return 0
            timesleep()
            ind+=1
    except (common.exceptions.ElementClickInterceptedException,common.exceptions.NoSuchElementException,common.exceptions.ElementNotInteractableException) as err:
        print(err)
        return 2


Webanketa_update()

#if __name__ == "__main__":
#    Webanketa_update()