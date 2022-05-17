import os
import fitz


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
    data = [None]*3
    data[0] = False
    doc=fitz.open(file)
    counter = 0
    while counter != doc.pageCount:
        try:
            base = str(doc.loadPage(counter).getText())
            if '''Основания для участия в конкурсе по результатам вступительных испытаний, проводимых МГУ для отдельных
категорий поступающих (вместо ЕГЭ)
1''' in doc.loadPage(0).getText():
                data[0] = True
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