from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, qApp
import keyboard as k
import time
import os
import sys
# translate ui to py
os.system("pyuic5 -x keyboard.ui -o uikeyboard.py")
time.sleep(1)
from uikeyboard import Ui_FlexiKey  # interface

hotkeys=dict()
abbreviations=dict()
combox=dict()
class Flexi(QtWidgets.QMainWindow):
    def __init__(self):
        super(Flexi, self).__init__()
        self.ui = Ui_FlexiKey()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('keyboard.png'))
        self.threading()
        for i in self.ui.cat1.findChildren(QtWidgets.QComboBox):
            i.addItems(["Bilgisayarı kapat","Hazırda beklet","cmd","Görev Yöneticisi","Website Aç",
            "Yeniden başlat","Çal/durdur","sonraki müzik","önceki müzik","Sağ tık","Sesi açma","Sesi kıs","Website ileri","Website geri","Mail","Ekran fotoğrafı","Sesi kapat"])
        #self.ui.pushButton.clicked.connect(self.button) #button connect
        self.tab1()
        self.tab2()
        self.tab3()
        self.tab4()
        self.tab5()

        for i in self.ui.centralwidget.findChildren(QtWidgets.QCheckBox):
            i.stateChanged.connect(self.updateCheckBox)

        for i in self.ui.cat1.findChildren(QtWidgets.QComboBox):
            i.currentTextChanged.connect(self.updateComboBox)

        for i in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            i.textChanged.connect(self.updateLineEdit)

        for i in self.ui.centralwidget.findChildren(QtWidgets.QKeySequenceEdit):
            i.keySequenceChanged.connect(self.updateKeySequenceEdit)


    def updateCheckBox(self):
        #cb=self.sender()
        self.tab1()
        self.tab2()
        self.tab3()
        self.tab4()
        self.tab5()

    def updateComboBox(self):
        #cb=self.sender()
        self.tab3()

    def updateLineEdit(self):
        #cb=self.sender()
        self.tab1()
        self.tab2()
        self.tab4()
        self.tab5()

    def updateKeySequenceEdit(self):
        #cb=self.sender()
        self.tab1()
        self.tab3()
        self.tab4()
        self.tab5()

    def tab1(self): #gridLayout1 = hotkey
        checkboxes=self.ui.cat1.findChildren(QtWidgets.QCheckBox)
        for checkbox in checkboxes:
            if(checkbox.isChecked()):
                for i in self.ui.cat1.findChildren(QtWidgets.QKeySequenceEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="x"):
                        i.setEnabled(True) 
                        shrtct=i
                        break
                for i in self.ui.cat1.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="x"): 
                        i.setEnabled(True)
                        line=i
                        break
                try:
                    a=shrtct.keySequence().toString().lower()
                    if(a=="" or line.text()=="" ):
                        pass
                    elif("," in a):
                        pass
                    else:
                        for i in hotkeys.items():
                            if(line.text()==i[1]):
                                del hotkeys[i[0]]
                                break
                        hotkeys[a.replace("^","3")]=line.text()
                except:pass
            else:   #the others will be disabled
                for i in self.ui.cat1.findChildren(QtWidgets.QKeySequenceEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="x"):
                        i.setDisabled(True)
                        break
                for i in self.ui.cat1.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="x"):
                        i.setDisabled(True)
                        for j in hotkeys.items():
                            if(i.text()==j[1]):
                                del hotkeys[j[0]]
                                try:
                                    k.remove_hotkey(j[0])
                                except:pass
                                break
                        break

    def tab2(self): #gridLayout2 = abbreviation
        checkboxes=self.ui.cat1.findChildren(QtWidgets.QCheckBox)
        for checkbox in checkboxes:
            if(checkbox.isChecked()):
                for i in self.ui.cat1.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="2" and checkbox.objectName()[-2:-1:]=="1"):
                        i.setEnabled(True)
                        shrtct=i
                        break
                for i in self.ui.cat1.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="1" and checkbox.objectName()[-2:-1:]=="1"):
                        i.setEnabled(True)
                        line=i
                        break
                try:
                    if(shrtct.text()=="" or line.text()=="" ):
                        pass
                    else:
                        for i in abbreviations.items():
                            if(line.text()==i[1]):
                                del abbreviations[i[0]]
                                k.remove_abbreviation(i[0])
                                break
                            if(shrtct.text()==i[0]):
                                k.remove_abbreviation(i[0])
                        abbreviations[shrtct.text()]=line.text()
                        k.add_abbreviation(shrtct.text(), line.text())
                except:pass
            else: 
                for i in self.ui.cat1.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="2" and checkbox.objectName()[-2:-1:]=="1"):
                        i.setDisabled(True)
                        break
                for i in self.ui.cat1.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="1" and checkbox.objectName()[-2:-1:]=="1"):
                        i.setDisabled(True)
                        for j in abbreviations.items():
                            if(i.text()==j[1]):
                                del abbreviations[j[0]]
                                k.remove_abbreviation(j[0])
                                break
                        break

    def tab3(self): #gridLayout3 = pc shortcuts
        checkboxes=self.ui.cat1.findChildren(QtWidgets.QCheckBox)
        combox.clear()
        for checkbox in checkboxes:
            if(checkbox.isChecked()):
                for i in self.ui.cat1.findChildren(QtWidgets.QComboBox):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="2" and i.objectName()[-2:-1:]=="x"): 
                        i.setEnabled(True)
                        combo=i
                        break
                for i in self.ui.cat1.findChildren(QtWidgets.QKeySequenceEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="2" and i.objectName()[-2:-1:]=="1"): 
                        i.setEnabled(True)
                        shrtct=i
                        break
                try:
                    if(combo.currentText=="" or shrtct.keySequence().toString().lower()==""):
                        pass
                    else:
                        combox[shrtct.keySequence().toString().lower()]=combo.currentText()
                except:pass
            else:   #the others will be disabled
                for i in self.ui.cat1.findChildren(QtWidgets.QComboBox):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="2"  and i.objectName()[-2:-1:]=="x"):
                        i.setDisabled(True)
                        break
                for i in self.ui.cat1.findChildren(QtWidgets.QKeySequenceEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="2" and i.objectName()[-2:-1:]=="1"):
                        i.setDisabled(True)
                        break

    def tab4(self): #gridLayout4
        checkboxes=self.ui.cat2.findChildren(QtWidgets.QCheckBox)
        for checkbox in checkboxes:
            if(checkbox.isChecked()):
                for i in self.ui.cat2.findChildren(QtWidgets.QKeySequenceEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="3" and i.objectName()[-2:-1:]=="2"): 
                        i.setEnabled(True) 
                        shrtct=i
                        break
                for i in self.ui.cat2.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="3" and i.objectName()[-2:-1:]=="3"): 
                        i.setEnabled(True) 
                        line=i
                        break
                try:
                    a=shrtct.keySequence().toString().lower()
                    if(a=="" or line.text()=="" ):
                        pass
                    elif("," in a):
                        pass
                    else:
                        for i in hotkeys.items():
                            if(line.text()==i[1]):
                                del hotkeys[i[0]]
                                break
                        hotkeys[a.replace("^","3")]=line.text()
                        #QTimer.singleShot(1000, self.wait(a.replace("^","3"),line.text()))
                except:pass
            else:   #the others will be disabled
                for i in self.ui.cat2.findChildren(QtWidgets.QKeySequenceEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="3" and i.objectName()[-2:-1:]=="2"): 
                        i.setDisabled(True)
                        break
                for i in self.ui.cat2.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and checkbox.objectName()[-2:-1:]=="3" and i.objectName()[-2:-1:]=="3"): 
                        i.setDisabled(True)
                        for j in hotkeys.items():
                            if(i.text()==j[1]):
                                del hotkeys[j[0]]
                                try:
                                    k.remove_hotkey(j[0])
                                except:pass
                                break
                        break

    def tab5(self): #gridLayout5
        checkboxes=self.ui.cat2.findChildren(QtWidgets.QCheckBox)
        for checkbox in checkboxes:
            if(checkbox.isChecked()):
                for i in self.ui.cat2.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="5" and checkbox.objectName()[-2:-1:]=="4"):
                        i.setEnabled(True)
                        shrtct=i
                        break
                for i in self.ui.cat2.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="4" and checkbox.objectName()[-2:-1:]=="4"):
                        i.setEnabled(True)
                        line=i
                        break
                try:
                    if(shrtct.text()=="" or line.text()=="" ):
                        pass
                    else:
                        for i in abbreviations.items():
                            if(line.text()==i[1]):
                                del abbreviations[i[0]]
                                k.remove_abbreviation(i[0])
                                break
                            if(shrtct.text()==i[0]):
                                k.remove_abbreviation(i[0])
                        abbreviations[shrtct.text()]=line.text()
                        k.add_abbreviation(shrtct.text(), line.text())
                except:pass
            else: 
                for i in self.ui.cat2.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="5" and checkbox.objectName()[-2:-1:]=="4"):
                        i.setDisabled(True)
                        break
                for i in self.ui.cat2.findChildren(QtWidgets.QLineEdit):
                    if(i.objectName()[-1::]==checkbox.objectName()[-1::] and i.objectName()[-2:-1:]=="4" and checkbox.objectName()[-2:-1:]=="4"):
                        i.setDisabled(True)
                        for j in abbreviations.items():
                            if(i.text()==j[1]):
                                del abbreviations[j[0]]
                                k.remove_abbreviation(j[0])
                                break
                        break

    def button(self):
        print(hotkeys)
        print(abbreviations)
        print(combox)
        #k.add_hotkey(self.ui.keySequenceEdit01.keySequence().toString(), lambda: k.write(self.ui.lineEdit01.text()))
        #k.add_hotkey('ctrl+alt+z',lambda: k.write('blablabla'))
        # print(self.ui.keySequenceEdit01.keySequence().toString())


        # Menubar interactive
        self.ui.menubar.triggered.connect(self.menuResponse)
    def menuResponse(self, action):
        if action.text() == "Minimize et":
            pass
        elif action.text() == "Çıkış":
            qApp.quit()

    def threading(self):    
        # create thread
        self.thread = QtCore.QThread()
        # create object which will be moved to another thread
        self.browserHandler = BrowserHandler()
        # move object to another thread
        self.browserHandler.moveToThread(self.thread)
        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.browserHandler.run)
        # start thread
        self.thread.start()

# Object, which will be moved to another thread
class BrowserHandler(QtCore.QObject):
    # method which will execute algorithm in another thread
    def run(self):
        # keyboard module thread run
        while True:
            a=k.read_hotkey(suppress=False)
            if(a in hotkeys):
                k.write(hotkeys[a])
            elif(a in combox):
                hotkey=combox[a]
                self.combobox(hotkey)
            else:pass
        k.wait()
    
    def combobox(self,hotkey):
        import pyautogui
        if(hotkey=="Bilgisayarı kapat"):
            os.system("shutdown -s")
        elif(hotkey=="Hazırda beklet"):
            os.system("shutdown -h")
        elif(hotkey=="Yeniden başlat"):
            os.system("shutdown -r")
        elif(hotkey=="Çal/durdur"):
            pyautogui.press("playpause")
        elif(hotkey=="Görev Yöneticisi"):
            pyautogui.hotkey('ctrl', 'shift', 'esc')
        elif(hotkey=="sonraki müzik"):
            pyautogui.hotkey('nexttrack')
        elif(hotkey=="önceki müzik"):
            pyautogui.hotkey('prevtrack')
        elif(hotkey=="cmd"):
            os.system("start cmd")
        elif(hotkey=="Website Aç"):
            os.system("start http://www.google.com")
        elif(hotkey=="Ekran fotoğrafı"):
            pyautogui.hotkey('prtsc')
        elif(hotkey=="Sağ tık"):
            pyautogui.hotkey('execute')
        elif(hotkey=="Website ileri"):
            pyautogui.hotkey('browserforward')
        elif(hotkey=="Website geri"):
            pyautogui.hotkey('browserback')
        elif(hotkey=="Mail"):
            pyautogui.hotkey('launchmail')
        elif(hotkey=="Sesi kapat"):
            pyautogui.hotkey('volumemute')
        elif(hotkey=="Sesi açma"):
            pyautogui.hotkey('volumeup')
        elif(hotkey=="Sesi kıs"):
            pyautogui.hotkey('volumedown')

app = QtWidgets.QApplication(sys.argv)
win = Flexi()
win.show()
sys.exit(app.exec_())
