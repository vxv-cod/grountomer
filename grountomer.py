from tkinter import E
from PyQt5 import QtCore, QtWidgets
import sys
from okno_ui import Ui_Form
import os
import interModul
from  vxv_tnnc_SQL_Pyton import Sql
os.system('CLS') 

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

_translate = QtCore.QCoreApplication.translate
Form.setWindowTitle(_translate("Form", "Grountomer"))

'''Уведомление'''
def SMS(Text, title='Ошибка'):
    QtWidgets.QMessageBox.information(Form, title, Text)

# -----------------------------------------------------------------------------
listXXX = ['Пески (кроме пылеватых)', 'Пески пылеватые', 'Супеси', 'Суглинки', 'Глины']

listYYY = [
        [''],
        [''],
        ['Lp ≤ 0,02', '0,02 < Lp ≤ 0,07'],
        ['0,07 < Lp ≤ 0,13','0,13 < Lp ≤ 0,17'],
        ['Lp > 0,17']
        ]

'''Задаем ведущий и подстраиваемый спиок'''
boxXXX = ui.comboBox_1
boxYYY = ui.comboBox_2

'''Список по умолчанию для для песков'''
boxYYY.setItemText(0, _translate("Form", listYYY[0][0]))
ui.comboBox_2.setEnabled(False)

def dependentList():
    ui.comboBox_2.setEnabled(True)
    index_boxXXX = boxXXX.currentIndex()
    for i in range(len(listYYY[index_boxXXX])):
        boxYYY.addItem("")
        boxYYY.setItemText(i, _translate("Form", listYYY[index_boxXXX][i]))
    if ui.comboBox_1.currentText() == "Пески (кроме пылеватых)":
        ui.comboBox_2.setEnabled(False)
    if ui.comboBox_1.currentText() == "Пески пылеватые":
        ui.comboBox_2.setEnabled(False)
    
# -----------------------------------------------------------------------------
'''Очищаем раскрывающийся список номеров сечения, чтобы не оставались предыдущие выборы списка'''
ui.comboBox_1.activated['QString'].connect(ui.comboBox_2.clear)
'''По выббранному профилю сечения меняем и список номеров сечения'''
ui.comboBox_1.activated['QString'].connect(dependentList)
# -----------------------------------------------------------------------------
def vvod(lineEditXXX, errorText):
    xxx = lineEditXXX.text()
    try:
        if xxx != '': 
            xxx = xxx.replace(',', '.')
        else: 
            xxx = 0
        xxx = float(xxx)
    except:
        SMS(errorText)
    return xxx

def SP25_13330_2020_Tab_B3():
    Sql("grountomer")
    errorText = 'СП 25.13330.2020_Таблица Б.3 - значение " T " от -0.3 до -15'
    lineEditXXX = ui.lineEdit
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return

    if -15 <= YYY <= -0.3:
        pass
    else:
        return SMS(errorText)

    YYY = abs(YYY)
    t1 = [-0.3, -0.5, -1.0, -2.0, -3.0, -4.0, -6.0, -8.0, -10.0, -15.0]
    t1 = [abs(i) for i in t1]
    t2All = [
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.50, 0.35, 0.30, 0.25, 0.23, 0.22, 0.21, 0.20, 0.19, 0.18],
            [0.50, 0.35, 0.30, 0.25, 0.23, 0.22, 0.21, 0.20, 0.19, 0.18],
            [0.60, 0.50, 0.40, 0.35, 0.32, 0.30, 0.27, 0.26, 0.25, 0.23],
            [0.70, 0.65, 0.58, 0.50, 0.46, 0.44, 0.42, 0.41, 0.40, 0.38],
            [0.80, 0.75, 0.65, 0.55, 0.51, 0.49, 0.47, 0.46, 0.45, 0.43],
            [0.98, 0.92, 0.80, 0.68, 0.63, 0.60, 0.57, 0.56, 0.55, 0.53]
            ]

    if boxXXX.currentText() == 'Пески (кроме пылеватых)': t2 = t2All[0]
    if boxXXX.currentText() == 'Пески пылеватые': t2 = t2All[1]
    if boxXXX.currentText() != 'Пески (кроме пылеватых)' and boxXXX != 'Пески пылеватые': 
        if boxYYY.currentText() == 'Lp ≤ 0,02': t2 = t2All[2]
        if boxYYY.currentText() == '0,02 < Lp ≤ 0,07': t2 = t2All[3]
        if boxYYY.currentText() == '0,07 < Lp ≤ 0,13': t2 = t2All[4]
        if boxYYY.currentText() == '0,13 < Lp ≤ 0,17': t2 = t2All[5]
        if boxYYY.currentText() == 'Lp > 0,17': t2 = t2All[6]

    Kw = interModul.interpoi(t1, t2, YYY, ui.lineEdit_2)
    ui.lineEdit_2.setText(str(Kw))
    

def SP22_13330_2016_Tab_51():
    Sql("grountomer")
    errorText = 'СП 22.13330.2016_Таблица 5.1 - значение " e " от 0.45 до 1.05'
    lineEditXXX = ui.lineEdit_4
    lineEditEnd = ui.lineEdit_3
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return
    if 0.45 <= YYY <= 1.05:
        pass
    else:
        return SMS(errorText)
    
    t1 = [0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05]
    t2All = [
            [2.8, 2.8, 2.5, 2.1, 1.4, "-", "-"],
            [3.0, 3.0, 2.7, 2.4, 2.0, 1.5, 1.0],
            ["-", "-", 2.4, 2.3, 2.2, 2.0, 1.8]
            ]

    boxXXX = ui.comboBox_4
    listXXX = ['Супеси', 'Суглинки', 'Глины']

    for i in range(len(listXXX)):
        if boxXXX.currentText() == listXXX[i]: 
            t2 = t2All[i]

    moed = interModul.interpoi(t1, t2, YYY, lineEditEnd)
    lineEditEnd.setText(str(moed))

def SP22_13330_2016_Tab_A1():
    Sql("grountomer")
    errorText = 'СП 22.13330.2016_Таблица А.1 - значение " e " от 0.45 до 0.75'
    lineEditXXX = ui.lineEdit_8
    lineEditEnd = [ui.lineEdit_7, ui.lineEdit_6, ui.lineEdit_5]
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return
    
    if 0.45 <= YYY <= 0.75:
        pass
    else:
        return SMS(errorText)

    t1 = [0.45, 0.55, 0.65, 0.75]

    t2All = [[
            [2.00, 1.00,"----","----"],
            [43.0, 40.0, 38.0,"----"],
            [50.0, 40.0, 30.0,"----"]
            ],[
            [3.00, 2.00, 1.00,"----"],
            [40.0, 38.0, 35.0,"----"],
            [50.0, 40.0, 30.0,"----"]
            ],[
            [6.00, 4.00, 2.00,"----"],
            [38.0, 36.0, 32.0, 28.0],
            [48.0, 38.0, 28.0, 18.0]
            ],[
            [8.00, 6.00, 4.00, 2.00],
            [36.0, 34.0, 30.0, 26.0],
            [39.0, 28.0, 18.0, 11.0]
            ]]

    boxXXX = ui.comboBox_5
    listXXX = ['Гравелистые и крупные', 'Средней крупности', 'Мелкие', 'Пылеватые']

    '''Для каждой из трех неизвестных'''
    for x in range(len(lineEditEnd)):
        '''Сверяем значение из таблицы со списком listXXX'''
        for i in range(len(listXXX)):
            if boxXXX.currentText() == listXXX[i]:
                '''вибираем нужный список из массива'''
                t2 = t2All[i][x]
                '''Интерполируем'''
                xxx = interModul.interpoi(t1, t2, YYY, lineEditEnd[x])
                '''отправляем релультат в таблицу'''
                lineEditEnd[x].setText(str(xxx))

def SP22_13330_2016_Tab_A2():
    Sql("grountomer")
    errorText = 'СП 22.13330.2016_Таблица А.2 - значение " e " от 0.45 до 1.05'
    lineEditXXX = ui.lineEdit_12
    lineEditEnd = [ui.lineEdit_9, ui.lineEdit_10]
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return
    if 0.45 <= YYY <= 1.05:
        pass
    else:
        return SMS(errorText)

    errorText = 'СП 22.13330.2016_Таблица А.2 - значение " IL " от 0 до 0.75'
    iL = vvod(ui.lineEdit_13, errorText)
    if isinstance(iL, str): return
    if 0.0 <= iL <= 0.75:
        pass
    else:
        return SMS('СП 22.13330.2016_Таблица А.2 - значение " IL " от 0 до 0.75')
    
    t1 = [0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05]

    
    t2All = [
            [
                [
                [21.0, 17.0, 15.0, 13.0,"----","----","----"],
                [30.0, 29.0, 27.0, 24.0,"----","----","----"]
                ],[
                [19.0, 15.0, 13.0, 11.0, 9.00,"----","----"],
                [28.0, 26.0, 24.0, 21.0, 18.0,"----","----"]
                ],[
                [19.0, 15.0, 13.0, 11.0, 9.00,"----","----"],
                [28.0, 26.0, 24.0, 21.0, 18.0,"----","----"]
                ]
            ],[
                [
                [47.0, 37.0, 31.0, 25.0, 22.0, 19.0,"----"],
                [26.0, 25.0, 24.0, 23.0, 22.0, 20.0,"----"]
                ],[
                [39.0, 34.0, 28.0, 23.0, 18.0, 15.0,"----"],
                [24.0, 23.0, 22.0, 21.0, 19.0, 17.0,"----"]
                ],[
                ["----","----", 25.0, 20.0, 16.0, 14.0, 12.0],
                ["----","----", 19.0, 18.0, 16.0, 14.0, 12.0]
                ]
            ],[
                [
                ["----", 81.0, 68.0, 54.0, 47.0, 41.0, 36.0],
                ["----", 21.0, 20.0, 19.0, 18.0, 16.0, 14.0]
                ],[
                ["----","----", 57.0, 50.0, 43.0, 37.0, 32.0],
                ["----","----", 18.0, 17.0, 16.0, 14.0, 11.0]
                ],[
                ["----","----", 45.0, 41.0, 36.0, 33.0, 29.0],
                ["----","----", 15.0, 14.0, 12.0, 10.0, 7.00]
                ]
            ]
            ]

    boxXXX = ui.comboBox_6
    listXXX = ['Супеси', 'Суглинки', 'Глины']
    # iL = ui.lineEdit_13.text()
    '''Для каждой из двух неизвестных'''
    for x in range(len(lineEditEnd)):
        '''Сверяем значение из таблицы со списком listXXX'''
        for i in range(len(listXXX)):
            if boxXXX.currentText() == listXXX[i]:
                '''вибираем нужный список из массива'''
                if 0 <= iL <= 0.25:
                    t2 = t2All[i][0][x]
                if 0.25 < iL <= 0.5:
                    t2 = t2All[i][1][x]
                if 0.5 < iL <= 0.75:
                    t2 = t2All[i][2][x]
                '''Интерполируем'''
                xxx = interModul.interpoi(t1, t2, YYY, lineEditEnd[x])
                '''отправляем релультат в таблицу'''
                lineEditEnd[x].setText(str(xxx))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def zamena(boxMen, listXXX_888):
    for i in range(len(listXXX_888)):
        boxMen.addItem("")
        boxMen.setItemText(i, _translate("Form", listXXX_888[i]))

def dependentList_A3_01():
    ui.comboBox_7.setEnabled(True)
    ui.comboBox_9.setEnabled(True)
    if ui.comboBox_8.currentText() == 'Четв.- ые':
        zamena(ui.comboBox_7, ['* аллюв-ые', 'Флювио-гляц.', 'Моренные'])
        zamena(ui.comboBox_9, ['Супеси', 'Суглинки', 'Глины'])
    if ui.comboBox_8.currentText() == 'Юрские':
        ui.comboBox_7.setEnabled(False)
        ui.comboBox_9.setEnabled(False)
        zamena(ui.comboBox_7, [""])
        zamena(ui.comboBox_9, ['Глины'])
    
def dependentList_A3_02():
    if ui.comboBox_7.currentText() == '* аллюв-ые':
        zamena(ui.comboBox_9, ['Супеси', 'Суглинки', 'Глины'])
    if ui.comboBox_7.currentText() == 'Флювио-гляц.':
        zamena(ui.comboBox_9, ['Супеси', 'Суглинки'])
    if ui.comboBox_7.currentText() == 'Моренные':
        zamena(ui.comboBox_9, ['Супеси', 'Суглинки'])
    if ui.comboBox_7.currentText() == '':
        zamena(ui.comboBox_9, ['Глины'])

ui.comboBox_8.activated['QString'].connect(ui.comboBox_7.clear)
ui.comboBox_8.activated['QString'].connect(ui.comboBox_9.clear)
ui.comboBox_8.activated['QString'].connect(dependentList_A3_01)
ui.comboBox_7.activated['QString'].connect(ui.comboBox_9.clear)
ui.comboBox_7.activated['QString'].connect(dependentList_A3_02)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def SP22_13330_2016_Tab_A3():
    Sql("grountomer")
    errorText = 'СП 22.13330.2016_Таблица А.3 - значение " e " от 0.35 до 1,6'
    lineEditXXX = ui.lineEdit_14
    lineEditEnd = [ui.lineEdit_15]
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return
    if 0.35 <= YYY <= 1.6:
        pass
    else:
        return SMS(errorText)

    errorText = 'СП 22.13330.2016_Таблица А.3 - значение " IL " от 0 до 0.75'
    iL = vvod(ui.lineEdit_16, errorText)
    if isinstance(iL, str): return
    
    if ui.comboBox_8.currentText() == 'Четв.- ые':
        if 0.0 <= iL <= 0.75:
            pass
        else:
            return SMS(errorText)
    
    if ui.comboBox_8.currentText() == 'Юрские':
        if -0.25 <= iL <= 0.5:
            pass
        else:
            return SMS('СП 22.13330.2016_Таблица А.3 - значение " IL " от -0.25 до 0.5')
    
    if ui.comboBox_7.currentText() == 'Моренные':
        if iL <= 0.5:
            pass
        else:
            return SMS('СП 22.13330.2016_Таблица А.3 - значение " IL " до 0.5')
    
    t1 = [0.35 , 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.2, 1.4, 1.6]
    t2All = [
            ["32.00", 32.00, 24.00, 16.00, 10.00, 7.00, "7.00", "7.00", "7.00", "7.00", "7.00"],  # 0
            
            ["34.00", 34.0000, 27.0000, 22.00, 17.00, 14.00, 11.00, "11.00","11.00","11.00","11.00"],  # 1
            ["32.00", 32.0000, 25.0000, 19.00, 14.00, 11.00,  8.00, "08.00", "08.00", "08.00", "08.00"],  # 2
            ["17.00","17.00","17.00", 17.00, 12.00, 8.00, 6.00, 5.0000, "5.000", "5.000", "5.000"],  # 3
            
            ["28.00", "28.00", 28.0000, 24.0000, 21.000, 18.00, 15.00, 12.00, "12.0","12.0","12.0"],  # 4
            ["21.00", "21.00", "21.00", 21.0000, 18.000, 15.00, 12.00, 9.00, "9.00", "9.00", "9.00"],  # 5
            ["15.00","15.00","15.00","15.00", 15.000, 12.00, 9.00, 7.00, "7.00", "7.00", "7.00"],  # 6
            
            ["33.00", 33.0000, 24.0000, 17.0000, 11.000, 7.00, "7.0", "7.00", "7.0", "7.00", "7.00"],  # 7
            
            ["40.00", 40.0000, 33.0000, 27.0000, 21.000, "21.0", "21.0", "21.0", "21.0", "21.0", "21.0"],  # 8
            ["35.00", 35.0000, 28.0000, 22.0000, 17.000, 14.000, "14.0","14.0","14.0","14.0","14.0"],  # 9
            ["17.00","17.00","17.00", 17.0000, 13.000, 10.000, 7.000, "7.00", "7.00", "7.00", "7.00"],  # 10
            
            [60.00, 50.00, 40.00, "40.0", "40.0", "40.0", "40.0", "40.0", "40.0", "40.0", "40.0"],  # 11

            ["27.00", "27.00", "27.00", "27.00", "27.00", "27.00", 27.0000, 25.0000, 22.00, "22.0", "22.0"],  # 12
            ["24.00", "24.00", "24.00", "24.00", "24.00", "24.00", 24.0000, 22.0000, 19.00, 15.000, "15.0"],  # 13
            ["16.00","16.00","16.00","16.00","16.00","16.00","16.00","16.00", 16.00, 12.000, 10.000]   # 14
            ]

    if ui.comboBox_8.currentText() == 'Четв.- ые':
        if ui.comboBox_7.currentText() == '* аллюв-ые':
            if ui.comboBox_9.currentText() == 'Супеси':
                if 0.0 <= iL <= 0.75: t2 = t2All[0]
            if ui.comboBox_9.currentText() == 'Суглинки':
                if 0.0 <= iL <= 0.25: t2 = t2All[1]
                if 0.25 < iL <= 0.50: t2 = t2All[2]
                if 0.50 < iL <= 0.75: t2 = t2All[3]
            if ui.comboBox_9.currentText() == 'Глины':
                if 0.0 <= iL <= 0.25: t2 = t2All[4]
                if 0.25 < iL <= 0.50: t2 = t2All[5]
                if 0.50 < iL <= 0.75: t2 = t2All[6]
        if ui.comboBox_7.currentText() == 'Флювио-гляц.':
            if ui.comboBox_9.currentText() == 'Супеси':
                if 0.0 <= iL <= 0.75: t2 = t2All[7]
            if ui.comboBox_9.currentText() == 'Суглинки':
                if 0.0 <= iL <= 0.25: t2 = t2All[8]
                if 0.25 < iL <= 0.50: t2 = t2All[9]
                if 0.50 < iL <= 0.75: t2 = t2All[10]
        if ui.comboBox_7.currentText() == 'Моренные':
            if iL <= 0.5:
                t2 = t2All[11]
            else:
                return SMS('СП 22.13330.2016_Таблица А.3 - значение " IL " от 0 до 0.50')
    if ui.comboBox_8.currentText() == 'Юрские':
        if -0.25 <= iL <= 0.0: t2 = t2All[12]
        if 0.000 <  iL <= 0.25: t2 = t2All[13]
        if 0.250 <  iL <= 0.50: t2 = t2All[14]
    
    '''Интерполируем'''
    xxx = interModul.interpoi(t1, t2, YYY, lineEditEnd[0])
    '''отправляем релультат в таблицу'''
    lineEditEnd[0].setText(str(xxx))

def SP22_13330_2016_Tab_A4():
    Sql("grountomer")
    errorText = 'СП 22.13330.2016_Таблица А.4 - значение " e " от 0.65 до 1.35'
    lineEditXXX = ui.lineEdit_19
    lineEditEnd = [ui.lineEdit_18, ui.lineEdit_17, ui.lineEdit_11]
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return
    if 0.65 <= YYY <= 1.35:
        pass
    else:
        return SMS(errorText)

    errorText = 'СП 22.13330.2016_Таблица А.4 - значение " IL " от 0 до 1.0'
    iL = vvod(ui.lineEdit_20, errorText)
    if isinstance(iL, str): return
    if 0.0 <= iL <= 1.0:
        pass
    else:
        return SMS(errorText)

    t1 = [0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35]

    t2All = [
            [
            [13.00, 12.00, 11.00, 10.00, 8.500, 8.000, 7.000, 5.000],
            [21.00, 20.00, 18.00, 16.00, 15.00,"----","----","----"],
            [29.00, 33.00, 37.00, 45.00, 48.00,"----","----","----"]
            ],
            [
            [11.00, 10.00,  8.50,  7.50,  7.00,  6.00,  5.50,  5.00],
            [21.00, 20.00, 18.00, 16.00, 15.00, 14.00, 13.00, 12.00],
            [21.00, 22.00, 24.00, 31.00, 33.00, 36.00, 39.00, 42.00]
            ],
            [
            [ 8.00,  7.00,  6.00,  5.50,  5.00,  5.00,  4.50,  4.00],
            [21.00, 20.00, 18.00, 16.00, 15.00, 14.00, 13.00, 12.00],
            [18.00, 19.00, 20.00, 21.00, 23.00, 24.00, 26.00, 28.00]
            ],
            [
            [ 6.00,  5.00,  4.50,  4.00,  3.50,  3.00,  2.500,"----"],
            ["---","----","----", 18.00, 18.00, 18.00, 17.00,"----"],
            ["---","----","----", 15.00, 16.00, 17.00, 18.00,"----"]
            ]
            ]

    for x in range(len(lineEditEnd)):
        if 0.00 <= iL <= 0.25:
            t2 = t2All[0][x]

        if 0.25 < iL <= 0.50:
            t2 = t2All[1][x]

        if 0.50 < iL <= 0.75:
            t2 = t2All[2][x]

        if 0.75 < iL <= 1.00:
            t2 = t2All[3][x]
        
        '''Интерполируем'''
        xxx = interModul.interpoi(t1, t2, YYY, lineEditEnd[x])
        '''отправляем релультат в таблицу'''
        lineEditEnd[x].setText(str(xxx))

def GOST_20522_2012_Tab_E2():
    Sql("grountomer")
    lineEditEnd = [ui.lineEdit_22]
    errorText = 'Число степеней свободы " K " от 3 до 60'
    K = vvod(ui.lineEdit_23, errorText)
    if isinstance(K, str): return
    if 3 <= K <= 60:
        pass
    else:
        return SMS(errorText)

    lineEditXXX = ui.lineEdit_21
    YYY = vvod(lineEditXXX, errorText)
    if isinstance(YYY, str): return

    if ui.radioButton.isChecked() == True:
        errorText = 'ГОСТ 20522-2012_Таблица Е.2 - значение " a " при односторонней доверительной вероятности  от 0.85 до 0.99'
        if 0.85 <= YYY <= 0.99:
            columnKey = [0.85, 0.90, 0.95, 0.975, 0.98, 0.99]
        else:
            return SMS(errorText)
        t1 = [0.85, 0.90, 0.95, 0.975, 0.98, 0.99]
    else:
        errorText = 'ГОСТ 20522-2012_Таблица Е.2 - значение " a " при двусторонней доверительной вероятности  от 0.70 до 0.98'
        if 0.7 <= YYY <= 0.98:
            columnKey = [0.70, 0.80, 0.90, 0.95, 0.96, 0.98]
        else:
            return SMS(errorText)

    RowKey =  [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 40, 60]

    columnValue = [
                [1.25, 1.19, 1.16, 1.13, 1.12, 1.11, 1.10, 1.10, 1.09, 1.08, 1.08, 1.08, 1.07, 1.07, 1.07, 1.07, 1.07, 1.06, 1.06, 1.05, 1.05, 1.05],
                [1.64, 1.53, 1.48, 1.44, 1.41, 1.40, 1.38, 1.37, 1.36, 1.36, 1.35, 1.34, 1.34, 1.34, 1.33, 1.33, 1.33, 1.32, 1.32, 1.31, 1.30, 1.30],
                [2.35, 2.13, 2.01, 1.94, 1.90, 1.86, 1.83, 1.81, 1.80, 1.78, 1.77, 1.76, 1.75, 1.75, 1.74, 1.73, 1.73, 1.72, 1.71, 1.70, 1.68, 1.67],
                [3.18, 2.78, 2.57, 2.45, 2.37, 2.31, 2.26, 2.23, 2.20, 2.18, 2.16, 2.15, 2.13, 2.12, 2.11, 2.10, 2.09, 2.09, 2.06, 2.04, 2.02, 2.00],
                [3.45, 3.02, 2.74, 2.63, 2.54, 2.49, 2.44, 2.40, 2.36, 2.33, 2.30, 2.28, 2.27, 2.26, 2.25, 2.24, 2.23, 2.22, 2.19, 2.17, 2.14, 2.12],
                [4.54, 3.75, 3.36, 3.14, 3.00, 2.90, 2.82, 2.76, 2.72, 2.68, 2.65, 2.62, 2.60, 2.58, 2.57, 2.55, 2.54, 2.53, 2.49, 2.46, 2.42, 2.39]
                ]
    
    xxx = interModul.GO(RowKey, columnKey, columnValue, K, YYY, ui.lineEdit_22)
    lineEditEnd[0].setText(str(xxx))


def SP25_13330_2020_Tab_B8():
    Sql("grountomer")
    print("\n")
    errorText = 'Исходные данные некорректны'
    Wtot = vvod(ui.lineEdit_26, errorText)
    if isinstance(Wtot, str): return
    Ro = vvod(ui.lineEdit_30, errorText)
    if isinstance(Ro, str): return
    # -------------------------------------------------------------------------------------
    Value_Pesok_Nezasol_Yth = [
                    ['----','----','1.91','1.91','1.91','1.91','1.91','1.57','----','----','----'],
                    ['----','----','1.91','1.91','1.91','1.91','1.91','1.57','----','----','----'],
                    ['----','----','----','----','1.91','1.91', 1.91 , 1.57 , 1.39 , 1.10 , 0.75 ],
                    ['----','----','----','----','----','2.50', 2.50 , 2.15 , 1.80 , 1.45 , 1.05 ],
                    ['----','----','----','----','----','----','2.67', 2.67 , 2.26 , 1.97 , 1.45 ],
                    ['----','----','----','----','----','----','----','2.67','2.26','1.97','1.45']
                    ]

    Value_Pesok_Nezasol_Yf = [
                    ['----','----','2.48','2.48','2.48','2.48','2.48','2.09','----','----','----'],
                    ['----','----','2.48','2.48','2.48','2.48','2.48','2.09','----','----','----'],
                    ['----','----', '--' ,'----','2.48','2.48', 2.48 , 2.09 , 1.83 , 1.35 , 0.84 ],
                    ['----','----', '--' ,'----','----','2.92', 2.92 , 2.50 , 2.10 , 1.68 , 1.16 ],
                    ['----','----', '--' ,'----','----','----','3.05', 3.05 , 2.75 , 2.30 , 1.56 ],
                    ['----','----', '--' ,'----','----','----','----','3.05','2.75','2.30','1.56']
                    ]

    Value_Pesok_Slabo_Yf = [                    
                    ["----","----","2.37","2.37","2.37","2.37",'2.37','2.00','----','----','----'],
                    ["----","----","2.37","2.37","2.37","2.37",'2.37','2.00','----','----','----'],
                    ["----","----","----","----","2.37","2.37", 2.37 , 2.00 , 1.75 , 1.30 , 0.82 ],
                    ["----","----","----","----","----","2.86", 2.86 , 2.43 , 2.03 , 1.62 , 1.10 ],
                    ["----","----","----","----","----","----","2.92", 2.92 , 2.63 , 2.23 , 1.52 ],
                    ["----","----","----","----","----","----","----",'2.92','2.63','2.23','1.52']
                    ]
    
    Value_Pesok_Sredne_Yf = [
                    ["----","----","2.21","2.21","2.21","2.21",'2.21','1.90','----','----','----'],
                    ["----","----","2.21","2.21","2.21","2.21",'2.21','1.90','----','----','----'],
                    ["----","----","----","----","2.21","2.21", 2.21 , 1.90 , 1.65 , 1.25 , 0.80 ],
                    ["----","----","----","----","----","2.78", 2.78 , 2.36 , 1.96 , 1.56 , 1.08 ],
                    ["----","----","----","----","----","----","2.80", 2.80 , 2.52 , 2.17 , 1.48 ],
                    ["----","----","----","----","----","----","----",'2.80','2.52','2.17','1.48']
                    ]
    
    Value_Pesok_Silno_Yf = [
                    ["----","----","2.08","2.08","2.08","2.08",'2.08','1.82','----','----','----'],
                    ["----","----","2.08","2.08","2.08","2.08",'2.08','1.82','----','----','----'],
                    ["----","----","----","----","2.08","2.08", 2.08 , 1.82 , 1.58 , 1.21 , 0.77 ],
                    ["----","----","----","----","----","2.70", 2.70 , 2.30 , 1.90 , 1.50 , 1.05 ],
                    ["----","----","----","----","----","----","2.69", 2.69 , 2.44 , 2.10 , 1.45 ],
                    ["----","----","----","----","----","----","----",'2.69','2.44','2.10','1.45'],
                    ]
    # -------------------------------------------------------------------------------------
    Value_Sypesi_Nezasol_Yth = [
                    ["1.80","1.80","----","----","----","----","----","----","----","----","----"],
                    ["1.80","1.80","1.80","----","----","----","----","----","----","----","----"],
                    ["1.80","1.80","1.80","1.80","----","----","----","----","----","----","----"],
                    ["----","----","1.80","1.80","----","----","----","----","----","----","----"],
                    ["----","----","----","1.80", 1.80 , 1.74 , 1.57 , 1.33 , 1.10 , 0.93 , 0.64 ],
                    ["----","----","----","----","1.80","1.80", 1.80 , 1.62 , 1.45 , 1.16 , 0.81 ],
                    ["----","----","----","----","----","1.86","1.86", 1.86 , 1.68 , 1.45 , 0.98 ],
                    ["----","----","----","----","----","----","----",'1.86','1.68','1.45','0.98'],
                    ]

    Value_Sypesi_Nezasol_Yf = [
                    [ 2.16 ,"2.14","----","----","----","----","----","----","----","----","----"],
                    ["2.16", 2.14 ,"2.10","----","----","----","----","----","----","----","----"],
                    ["2.16","2.14", 2.10 ,"2.02","----","----","----","----","----","----","----"],
                    ["----","----","2.10", 2.02 ,"2.00","1.98","1.84","1.63","1.35","1.09","0.73"],
                    ["----","----","----","2.02", 2.00 , 1.98 , 1.84 , 1.63 , 1.35 , 1.09 , 0.73 ],
                    ["----","----","----","----","2.00","2.00", 2.00 , 1.78 , 1.60 , 1.29 , 0.87 ],
                    ["----","----","----","----","----","----","2.05", 2.05 , 1.83 , 1.59 , 0.99 ],
                    ["----","----","----","----","----","----","2.05",'2.05','1.83','1.59','0.99']
                    ]

    Value_Sypesi_Slabo_Yf = [
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],

                    ["----","----","1.95","1.95","1.95","1.95","1.81","1.58","----","----","----"],
                    ["----","----","----","1.95","1.95",'1.95','1.81','1.58','1.30','1.06','0.71'],
                    ["----","----","----","----","1.95", 1.95 , 1.81 , 1.58 , 1.30 , 1.06 , 0.71 ],
                    ["----","----","----","----","----","1.96", 1.96 , 1.75 , 1.56 , 1.26 , 0.85 ],
                    ["----","----","----","----","----","----","2.00", 2.00 , 1.79 , 1.55 , 0.98 ],
                    ["----","----","----","----","----","----","2.00",'2.00','1.79','1.55','0.98']
                    ]

    Value_Sypesi_Sredne_Yf = [
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    
                    ["1.91","1.91","1.91","1.91","1.91",'1.91','1.78','1.53','----','----','----'],
                    ["----","----","----","----","1.91",'1.91','1.78','1.53','1.25','1.03','0.69'],
                    ["----","----","----","----","1.91", 1.91 , 1.78 , 1.53 , 1.25 , 1.03 , 0.69 ],
                    ["----","----","----","----","----","1.92", 1.92 , 1.71 , 1.52 , 1.22 , 0.84 ],
                    ["----","----","----","----","----","----","1.94", 1.94 , 1.74 , 1.51 , 0.98 ],
                    ["----","----","----","----","----","----","1.94",'1.94','1.74','1.51','0.98']
                    ]
  
    Value_Sypesi_Silno_Yf = [
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],

                    ["1.88","1.88","1.88","1.88","1.88",'1.88','1.73','1.48','----','----','----'],
                    ["----","----","----","----","1.88",'1.88','1.73','1.48','----','----','----'],
                    ["----","----","----","----","1.88", 1.88 , 1.73 , 1.48 , 1.20 , 0.99 , 0.67 ],
                    ["----","----","----","----","----","1.88", 1.88 , 1.67 , 1.49 , 1.19 , 0.82 ],
                    ["----","----","----","----","----","----","1.88", 1.88 , 1.70 , 1.47 , 0.97 ],
                    ["----","----","----","----","----","----","1.88",'1.88','1.70','1.47','0.97']
                    ]
    # -------------------------------------------------------------------------------------            
    Value_Glins_Nezasol_Yth = [
                    ["1.57","1.57","----","----","----","----","----","----","----","----","----"],
                    ["1.57","1.57","1.57","----","----","----","----","----","----","----","----"],
                    ["1.57","1.57","1.57","1.57","----","----","----","----","----","----","----"],
                    ["----","----","1.57", 1.57 ,'1.57','1.45','1.33','1.10','0.87','0.70','0.46'],
                    ["----","----","----","1.57", 1.57 , 1.45 , 1.33 , 1.10 , 0.87 , 0.70 , 0.46 ],
                    ["----","----","----","----","1.68", 1.68 , 1.51 , 1.33 , 1.10 , 0.87 , 0.58 ],
                    ["----","----","----","----","----",'1.57','1.57', 1.57 , 1.39 , 1.06 , 0.70 ],
                    ["----","----","----","----","----","----",'1.57','1.57','1.28', 1.28 ,'1.28']
                    ]

    Value_Glins_Nezasol_Yf = [
                    [ 2.10 ,"2.00","----","----","----","----","----","----","----","----","----"],
                    ["2.10", 2.00 ,"1.90","----","----","----","----","----","----","----","----"],
                    ["2.10","2.00", 1.90 ,"1.80","----","----","----","----","----","----","----"],
                    ["----","----","1.90", 1.80 ,'1.76','1.65','1.58','1.31','0.99','0.77','0.48'],
                    ["----","----","----","1.80", 1.76 , 1.65 , 1.58 , 1.31 , 0.99 , 0.77 , 0.48 ],
                    ["----","----","----","----","1.94", 1.94 , 1.75 , 1.56 , 1.23 , 0.97 , 0.60 ],
                    ["----","----","----","----","----","----","1.86", 1.86 , 1.60 , 1.26 , 0.75 ],
                    ["----","----","----","----","----","----","1.86","1.86","1.46", 1.46 ,"1.46"]
                    ]

    Value_Glins_Slabo_Yf = [
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    
                    ["1.68","1.68","1.68","1.68","1.68",'1.59','1.50','1.23','0.94','0.75','0,43'],
                    ["----","----","----","1.68", 1.68 , 1.59 , 1.50 , 1.23 , 0.94 , 0.75 , 0,43 ],
                    ["----","----","----","----","1.80", 1.80 , 1.68 , 1.46 , 1.17 , 0.92 , 0,56 ],
                    ["----","----","----","----","----","----","1.70", 1.70 , 1.47 , 1.14 , 0,69 ],
                    ["----","----","----","----","----","----","----","1.70","1.35", 1.35 ,"1.35"]
                    ]

    Value_Glins_Sredne_Yf = [
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    
                    ["1.65","1.65","1.65","1.65",'1.65','1.56','1.46','1.20','0.92','0.73','0,41'],
                    ["----","----","----","1.65", 1.65 , 1.56 , 1.46 , 1.20 , 0.92 , 0.73 , 0,41 ],
                    ["----","----","----","----","1.74", 1.74 , 1.62 , 1.41 , 1.15 , 0.90 , 0,55 ],
                    ["----","----","----","----","----","----","1.61", 1.61 , 1.40 , 1.09 , 0,68 ],
                    ["----","----","----","----","----","----","----","----","1.30", 1.30 ,"1.30"]
                    ]

    Value_Glins_Silno_Yf = [
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    ["----","----","----","----","----","----","----","----","----","----","----"],
                    
                    ["1.59","1.59","1.59","1.59",'1.59','1.50','1.36','1.10','0.87','0.71','0,40'],
                    ["----","----","----","1.59", 1.59 , 1.50 , 1.36 , 1.10 , 0.87 , 0.71 , 0,40 ],
                    ["----","----","----","----","1.65", 1.65 , 1.49 , 1.30 , 1.08 , 0.86 , 0,53 ],
                    ["----","----","----","----","----","----","1.48", 1.48 , 1.36 , 1.02 , 0,65 ],
                    ["----","----","----","----","----","----","----","----","1.25", 1.25 ,"1.25"]
                    ]
    # -------------------------------------------------------------------------------------
    Value_Torfs_Yth = [
                    [ 0.810 , 0.400 , 0.230 , 0.175 , 0.120 ],
                    ["0.810","0.400", 0.810 , 0.520 , 0.230 ],
                    ["-----","-----","0.810", 0.930 , 0.410 ],
                    ["-----","-----","-----","0.930", 0.930 ]
                    ]
    
    Value_Torfs_Yf = [
                    [ 1.340 , 0.700 , 0.410 , 0.320 , 0.230 ],
                    ["-----","0.700", 1.330 , 0.925 , 0.520 ],
                    ["-----","-----","1.330", 1.390 , 0.700 ],
                    ["-----","-----","-----","1.390", 1.390]
                    ]
    # -------------------------------------------------------------------------------------
    def perevorotTab(xxx):
        res = []
        for i in range(len(xxx[0])):
            zzz = []
            for x in range(len(xxx)):
                zzz.append(xxx[x][i])
            res.append(zzz)
        return res

    # RowKey_1 = [1.4, 1.6, 1.8, 2.0]
    RowKey_1 = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    RowKey_2 = [0.4, 0.7, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    columnKey_netor = [2.00, 1.00, 0.60, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05]
    RowKey_torf = [0.1, 0.2, 0.3, 0.4]
    columnKey_totfs = [9.0, 6.0, 4.0, 3.0, 2.0]

    def work(RowKey, columnKey, Value_Yth, Value, Ro, Wtot):
        if ui.comboBox_12.currentText() != 'Заторфованные, торф':
            if Wtot > 2.0 or Wtot < 0.05: return SMS("Суммарная влажность 0.05 ≤ Wtot ≤ 2.0")
            if Ro < 0.4 or Ro > 2.0: return SMS("Плотность сухого грунта 0.4 ≤ ρ ≤ 2.0")
        try:
            xxx = interModul.GO(RowKey, columnKey, perevorotTab(Value_Yth), Ro, Wtot, ui.lineEdit_27)
        except:
            xxx = "-"
        ui.lineEdit_27.setText(str(xxx))
        xxx = interModul.GO(RowKey, columnKey, perevorotTab(Value), Ro, Wtot, ui.lineEdit_28)
        ui.lineEdit_28.setText(str(xxx))

    triger = False
    if Wtot < 0.05:
        Wtot = 0.05
        triger = True

    if ui.comboBox_12.currentText() == 'Пески разной плотности':
        if ui.comboBox_11.currentText() == 'Незасоленные': work(RowKey_1, columnKey_netor, Value_Pesok_Nezasol_Yth, Value_Pesok_Nezasol_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Слабо засоленные': work(RowKey_1, columnKey_netor, None, Value_Pesok_Slabo_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Средне засоленные': work(RowKey_1, columnKey_netor, None, Value_Pesok_Sredne_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Сильно засоленные': work(RowKey_1, columnKey_netor, None, Value_Pesok_Silno_Yf, Ro, Wtot)

    if ui.comboBox_12.currentText() == 'Супеси пылеватые':
        if ui.comboBox_11.currentText() == 'Незасоленные': work(RowKey_2, columnKey_netor, Value_Sypesi_Nezasol_Yth, Value_Sypesi_Nezasol_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Слабо засоленные': work(RowKey_2, columnKey_netor, None, Value_Sypesi_Slabo_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Средне засоленные': work(RowKey_2, columnKey_netor, None, Value_Sypesi_Sredne_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Сильно засоленные': work(RowKey_2, columnKey_netor, None, Value_Sypesi_Silno_Yf, Ro, Wtot)
    
    if ui.comboBox_12.currentText() == 'Суглинки и глины':
        if ui.comboBox_11.currentText() == 'Незасоленные': work(RowKey_2, columnKey_netor, Value_Glins_Nezasol_Yth, Value_Glins_Nezasol_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Слабо засоленные': work(RowKey_2, columnKey_netor, None, Value_Glins_Slabo_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Средне засоленные': work(RowKey_2, columnKey_netor, None, Value_Glins_Sredne_Yf, Ro, Wtot)
        if ui.comboBox_11.currentText() == 'Сильно засоленные': work(RowKey_2, columnKey_netor, None, Value_Glins_Silno_Yf, Ro, Wtot)
    
    if ui.comboBox_12.currentText() == 'Заторфованные, торф':
        if Wtot < 2.0 or Wtot > 9.0: return SMS("Суммарная влажность 2.0 ≤ Wtot ≤ 9.0")
        if Ro < 0.1 or Ro > 0.4: return SMS("Плотность сухого грунта 0.1 ≤ ρ ≤ 0.4")
        work(RowKey_torf, columnKey_totfs, Value_Torfs_Yth, Value_Torfs_Yf, Ro, Wtot)

    if triger == True:
        ui.lineEdit_27.setStyleSheet("background-color: rgb(255, 170, 0);")
        ui.lineEdit_28.setStyleSheet("background-color: rgb(255, 170, 0);")
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def dependentList_B8():
    ui.comboBox_11.setEnabled(True)
    if ui.comboBox_12.currentText() != 'Заторфованные, торф':
        zamena(ui.comboBox_11, ["Незасоленные", "Слабо засоленные", "Средне засоленные", "Сильно засоленные"])
    else:
        ui.comboBox_11.setEnabled(False)
        zamena(ui.comboBox_11, [""])

ui.comboBox_12.activated['QString'].connect(ui.comboBox_11.clear)
ui.comboBox_12.activated['QString'].connect(dependentList_B8)
# -----------------------------------------------------------------------------
def openSP():
    '''файл откроется в приложении Microsoft Word'''
    os.startfile('Tables.docx', 'edit')
# -----------------------------------------------------------------------------
ui.pushButton.clicked.connect(SP25_13330_2020_Tab_B3)
ui.pushButton_2.clicked.connect(SP22_13330_2016_Tab_51)
ui.pushButton_3.clicked.connect(SP22_13330_2016_Tab_A1)
ui.pushButton_4.clicked.connect(SP22_13330_2016_Tab_A2)
ui.pushButton_5.clicked.connect(SP22_13330_2016_Tab_A3)
ui.pushButton_6.clicked.connect(SP22_13330_2016_Tab_A4)
ui.pushButton_7.clicked.connect(GOST_20522_2012_Tab_E2)
ui.pushButton_9.clicked.connect(SP25_13330_2020_Tab_B8)
ui.pushButton_8.clicked.connect(openSP)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(app.exec_())