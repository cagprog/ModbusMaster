import serial
import threading
from datetime import datetime
import pk #pyuic5 pk.ui -o pk.py
import modbusmaslib
#import sys,glob #for listing serial ports
import serial.tools.list_ports  #for listing serial ports


#TODO:
#online olmayan cihazlar her dongüde sorgulanmayacak.
#8-10 dongude bir sorgulanacak.boylece hız kazanılacak...
#birden fazla cihaz offline ise her döngüde bir adet sorgulanacak.
#testval=True

serial_port_list=[]
serial_hwid_list=[]
selected_port=''
port_selected=False
quit_program=False
default_serial_port_loc='LOCATION=1-2.2'  #default serial port location

class displayForm(pk.Ui_Form):
    def setupUiChield(self,Form):
        self.setupUi(Form)
        self.model = pk.QtGui.QStandardItemModel()
        self.listView.setModel(self.model)#listView görmek için......

        self.pushButton_1.setText("Exit")
        self.pushButton_1.clicked.connect(self.klik1)
     
        self.portSelectBox.activated.connect(self.compSelClick)

    def goster(self,entry):
        item = pk.QtGui.QStandardItem(str(entry))
        self.model.appendRow(item)

    def klik1(self):
        global quit_program
        self.goster('Exit')
        quit_program=True
        testval=False #TODO neden tanımıyor ?????
        sys.exit(0)

    def compSelClick(self):
        global port_selected
        global selected_port

        selected_port=serial_port_list[self.portSelectBox.currentIndex()]
        print(selected_port,'  Seçildi')
        self.portSelectBox.setEnabled(False)
        port_selected=True
        myserialPort = serial.Serial(selected_port, baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,timeout=1)
        for x in slvArray:
            x.serialObj=myserialPort
        
    def setportlist(self):
        self.portSelectBox.clear()
        self.portSelectBox.addItems(serial_hwid_list)
    
    #TODO conn.close() olacakmı

class slvModules(modbusmaslib.slvDevice):
    def __init__(self,adresxx):
        super().__init__(adresxx)
        """self.serial.baudrate=19200
        self.serial.parity=serial.PARITY_EVEN
        self.serial.bytesize=serial.EIGHTBITS
        self.serial.stopbits=serial.STOPBITS_ONE
        self.serial.timeout = 1"""

def anaDongu():
    dtonceki=0
    loopPeriod=0.1 #sn.
    msgInterval=0.01 #sn.
    global quit_program
    global port_selected

    def func3g(slvD,a,d):   #Read n words: function 3
        #print('***************')
        mesaj='Query>>> f:3(read n w) mdA: {}  dA: {}  nr: {}'.format(slvD.mdbsAdress,a,d)
        ui.goster(mesaj)
        response=slvD.func3(slvD.mdbsAdress,a,d)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response
    def func6g(slvD,address,data): #write a word
        mesaj='Query>>> f:6(write a word) mdA: {}  dA: {}  data: {}'.format(slvD.mdbsAdress,address,data)
        ui.goster(mesaj)
        response=slvD.func6(slvD.mdbsAdress,address,data)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response
    def func8g(slvD,subfunccode): #diagnostic
        mesaj='Query>>> f:8(diagnostic) mdA: {}  sub func: {}  '.format(slvD.mdbsAdress,subfunccode)
        ui.goster(mesaj)
        response=slvD.func8(slvD.mdbsAdress,subfunccode)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response
    def func16g(slvD,dataaddress,datalist): #Write n consecutive words: function 16
        mesaj='Query>>> f:16(Write n consecutive words) mdA: {}  dataadres {}  datalist: {}  '.format(slvD.mdbsAdress,dataaddress,datalist)
        ui.goster(mesaj)
        response=slvD.func16(slvD.mdbsAdress,dataaddress,datalist)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response


    while (not quit_program):
        #print(port_selected)
        if port_selected:
            for slvDev in slvArray:
                #print(slvDev.mdbsAdress)
                try:
                    t1=func3g(slvDev,10,5)
                    t2=func3g(slvDev,10,2)
                    t61=func6g(slvDev,20,30)
                    t81=func8g(slvDev,0)
                    t161=func16g(slvDev,50,[256,257,258])
                except modbusmaslib.NoResponseError:
                    mesaj='        {} adresinde hata ....cevap yok '.format(slvDev.mdbsAdress)
                    #print("hata cevap gelmedi...")
                    ui.goster(mesaj)
                except modbusmaslib.InvalidResponseError:
                    print ('modbuslib.InvalidResponseError:  hatası...')
                except modbusmaslib.comPortError:
                    #sudo chmod a+rw /dev/ttyUSB1  yapılmazsa bu hatayı veriyor.
                    #alt satırdaki gibi de izin verilebilir...
                    #import subprocess
                    #subprocess.Popen(["sudo", "chmod", "666", "/dev/ttyUSB0"], stdout=subprocess.PIPE, shell=True)
                    print('modbusmaslib.comPortError    hatası...')
                    port_selected=False
                    ui.portSelectBox.setEnabled(True)
                    serial_ports()
                    ui.setportlist()
                ui.goster(str(round(datetime.timestamp(datetime.now())-dtonceki,2)))
                dtonceki=datetime.timestamp(datetime.now())
        else:
            if not 'prevList' in locals():
                prevList=[]
            serial_ports()
            if set(serial_port_list)!=set(prevList):
                ui.setportlist()
            prevList=serial_port_list.copy()

def serial_ports():
    global serial_port_list #method içinden ulaşmak için 'global' kullanılmalı
    global serial_hwid_list
    #*****  Lists serial port names  *****
    ports = serial.tools.list_ports.comports()
    serial_port_list = []
    serial_hwid_list=[]
    for port, desc, hwid in sorted(ports):
        serial_port_list.append(port)
        serial_hwid_list.append(hwid)
 
if __name__ == "__main__":
    # pk.py main den alındı .. form göster******************
    import sys
    testval=True

    app = pk.QtWidgets.QApplication(sys.argv)
    Form = pk.QtWidgets.QWidget()
    ui = displayForm()
    ui.setupUiChield(Form)
    Form.show()
    #          list serial ports
    serial_ports()
    print(serial_port_list)
    ui.setportlist()

    #***Build slave list***
    slvArray=[]
    slvArray.append(slvModules(1))
    slvArray.append(slvModules(2))
    slvArray.append(slvModules(3))

    for indks in range(len(serial_hwid_list)):   # port, desc, hwid in sorted(ports):
        if default_serial_port_loc in serial_hwid_list[indks]:
            selected_port=serial_port_list[indks]
            print(selected_port,' Seçildi..')
            port_selected=True
            ui.portSelectBox.setEnabled(False)
            myserialPort = serial.Serial(selected_port, baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,timeout=1)
            for x in slvArray:
                x.serialObj=myserialPort

    dongu=threading.Thread(target=anaDongu)
    dongu.start()
    sys.exit(app.exec_()) #form gostermek için