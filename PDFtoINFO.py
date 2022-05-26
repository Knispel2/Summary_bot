import os
import fitz

reg_zones={'АгинскийБурятскийАОнеиспользуется': 'MSK+6', 'АдыгеяРесп': 'MSK+0', 'АлтайРесп': 'MSK+4', 'Алтайскийкрай': 'MSK+4', 
           'Амурскаяобл': 'MSK+6', 'Архангельскаяобл': 'MSK+0', 'Астраханскаяобл': 'MSK+1', 'Байконург': 'MSK+3', 
           'БашкортостанРесп': 'MSK+2', 'Белгородскаяобл': 'MSK+0', 'Брянскаяобл': 'MSK+0', 'БурятияРесп': 'MSK+5', 
           'Владимирскаяобл': 'MSK+0', 'Волгоградскаяобл': 'MSK+0', 'Вологодскаяобл': 'MSK+0', 'Воронежскаяобл': 'MSK+0', 
           'ДагестанРесп': 'MSK+0', 'ЕврейскаяАобл': 'MSK+7', 'Забайкальскийкрай': 'MSK+6', 'Ивановскаяобл': 'MSK+0', 
           'ИнгушетияРесп': 'MSK+0', 'Иркутскаяобл': 'MSK+5', 'Кабардино-БалкарскаяРесп': 'MSK+0', 'Калининградскаяобл': 'MSK-1', 
           'КалмыкияРесп': 'MSK+0', 'Калужскаяобл': 'MSK+0', 'Камчатскийкрай': 'MSK+9', 'Карачаево-ЧеркесскаяРесп': 'MSK+0', 
           'КарелияРесп': 'MSK+0', 'Кемеровскаяобл': 'MSK+4', 'Кировскаяобл': 'MSK+0', 'КомиРесп': 'MSK+0', 'Коми-ПермяцкийАО': 'MSK+2', 
           'Костромскаяобл': 'MSK+0', 'Краснодарскийкрай': 'MSK+0', 'Красноярскийкрай': 'MSK+4', 'Крымресп.': 'MSK+0', 
           'Курганскаяобл': 'MSK+2', 'Курскаяобл': 'MSK+0', 'Ленинградскаяобл': 'MSK+0', 'Липецкаяобл': 'MSK+0', 
           'Магаданскаяобл': 'MSK+7', 'МарийЭлРесп': 'MSK+0', 'МордовияРесп': 'MSK+0', 'Москваг': 'MSK+0', 
           'Московскаяобл': 'MSK+0', 'Мурманскаяобл': 'MSK+0', 'НенецкийАО': 'MSK+0', 'Нижегородскаяобл': 'MSK+0', 
           'Новгородскаяобл': 'MSK+0', 'Новосибирскаяобл': 'MSK+3', 'Омскаяобл': 'MSK+3', 'Оренбургскаяобл': 'MSK+2', 
           'Орловскаяобл': 'MSK+0', 'Пензенскаяобл': 'MSK+0', 'Пермскийкрай': 'MSK+2', 'Приморскийкрай': 'MSK+7', 
           'Псковскаяобл': 'MSK+0', 'Ростовскаяобл': 'MSK+0', 'Рязанскаяобл': 'MSK+0', 'Самарскаяобл': 'MSK+1', 
           'Санкт-Петербургг': 'MSK+0', 'Саратовскаяобл': 'MSK+0', 'Саха/Якутия/Респ': 'MSK+6/7/8', 'Сахалинскаяобл': 'MSK+8', 
           'Свердловскаяобл': 'MSK+2', 'СЕВАСТОПОЛЬ': 'MSK+0', 'СевернаяОсетия-АланияРесп': 'MSK+0', 'Смоленскаяобл': 'MSK+0', 
           'Ставропольскийкрай': 'MSK+0', 'Таймырский(Долгано-Ненецкий)АО': 'MSK+4', 'Тамбовскаяобл': 'MSK+0', 
           'ТатарстанРесп': 'MSK+0', 'Тверскаяобл': 'MSK+0', 'Томскаяобл': 'MSK+3', 'Тульскаяобл': 'MSK+0', 'ТываРесп': 'MSK+4', 
           'Тюменскаяобл': 'MSK+2', 'УдмуртскаяРесп': 'MSK+1', 'Ульяновскаяобл': 'MSK+1', 'Усть-ОрдынскийБурятскийАО': 'MSK+5',
          'Хабаровскийкрай': 'MSK+7', 'ХакасияРесп': 'MSK+4', 'Ханты-МансийскийАО': 'MSK+2', 'Челябинскаяобл': 'MSK+2', 
          'ЧеченскаяРесп': 'MSK+0', 'ЧувашскаяРесп': 'MSK+0', 'ЧукотскийАО': 'MSK+9', 'ЭвенкийскийАО': 'MSK+4', 
          'Ямало-НенецкийАО': 'MSK+2', 'Ярославскаяобл': 'MSK+0'}


def PDFtoINFO(file):
    try:        
        data = [None]*3
        doc=fitz.open(file) #кряк с директорией
        base = str(doc.loadPage(2).getText())
        print(base)
        if 'Фундаментальная математика и механика' in doc.loadPage(0).getText() and 'ОСОБАЯ КВОТА' not in doc.loadPage(0).getText():
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
            if 'ОСОБАЯ КВОТА' in doc.loadPage(0).getText():
                counter = 0
                while counter != doc.pageCount:
                    try:
                        base = str(doc.loadPage(counter).getText())
                        if 'КОНТАКТНЫЕ ТЕЛЕФОНЫ (городской с кодом города и мобильный) И АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ' in doc.loadPage(counter).getText():
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
                        if '''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
(при наличии)''' in doc.loadPage(counter).getText():
                            j = base.find('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
(при наличии)''')
                            start = 1 + j + len('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
(при наличии)''')
                            buf2 = []
                            while(base[start] != 'С') and (base[start] != '_'):
                                if base[start] not in {'\n', ' '}:
                                    buf2.append(base[start])
                                start+=1
                            data[2] = ''.join(buf2)
                        counter+=1
                    except:
                        break
                return data
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
    except Exception as err:
        print('*',err,'*')
        return data
    data[1] = ''.join(i for i in data[1] if not i.isalpha())
    print(str(doc.loadPage(3).getText()))
    return data

def PDFtoINFO_brute(file):
    data = [None]*4
    data[0] = False
    doc=fitz.open(file)
    counter = 0
    while counter != doc.pageCount:
        try:
            #print(doc.loadPage(counter).getText())
            base = str(doc.loadPage(counter).getText())
            if '''Основания для участия в конкурсе по результатам вступительных испытаний, проводимых МГУ для отдельных
категорий поступающих (вместо ЕГЭ)
1''' in doc.loadPage(0).getText():
                data[0] = True
            if 'ДЛЯ РОССИИ - НАЗВАНИЕ СУБЪЕКТА ФЕДЕРАЦИИ' in doc.loadPage(counter).getText():
                j = base.find('ДЛЯ РОССИИ - НАЗВАНИЕ СУБЪЕКТА ФЕДЕРАЦИИ')
                start = 2 + j + len('ДЛЯ РОССИИ - НАЗВАНИЕ СУБЪЕКТА ФЕДЕРАЦИИ')
                buf = []
                indicator = '2'
                while(base[start] != indicator):
                    if base[start] not in {'\n', ' '}:
                        buf.append(base[start])
                    start+=1
                data[3] = reg_zones[''.join(buf)]
            if 'КОНТАКТНЫЕ ТЕЛЕФОНЫ (городской с кодом города и мобильный) И АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ' in doc.loadPage(counter).getText():
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
                data[1] = ''.join(i for i in data[1] if (not i.isalpha()) and (not i in {'@'}))
            if '''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
(при наличии)''' in doc.loadPage(counter).getText():
                     j = base.find('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
(при наличии)''')
                     start = 1 + j + len('''НОМЕР СТРАХОВОГО СВИДЕТЕЛЬСТВА ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО СТРАХОВАНИЯ РФ
(при наличии)''')
                     buf2 = []
                     while(base[start] != 'С') and (base[start] != '_'):
                         if base[start] not in {'\n', ' '}:
                             buf2.append(base[start])
                         start+=1
                     data[2] = ''.join(buf2)
            counter+=1
        except:
            break
    return data


#folder='C:/FSR_Data/'
#print(PDFtoINFO_brute(folder + 'кирдин_св_21547.pdf'))
#input()