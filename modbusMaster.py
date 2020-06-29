import serial
import threading
from datetime import datetime
import pk 
import modbusmaslib
import serial.tools.list_ports  #for listing serial ports

serial_port_list=[]
serial_hwid_list=[]
selected_port=''
port_selected=False
quit_program=False

default_serial_port_loc='LOCATION=1-2.2'  #default serial port location

class displayForm(pk.Ui_Form):
    enable_display=True
    def setupUiChield(self,Form):
        self.setupUi(Form)
        self.model = pk.QtGui.QStandardItemModel()
        self.listView.setModel(self.model)#to see listView ......

        self.pushButton_1.setText("Exit")
        self.pushButton_1.clicked.connect(self.klik1)

        
        self.pushButton_2.clicked.connect(self.klik2)
     
        self.portSelectBox.activated.connect(self.compSelClick)

    def goster(self,entry):
        if self.enable_display:
            item = pk.QtGui.QStandardItem(str(entry))
            self.model.appendRow(item)

    def klik1(self):
        global quit_program
        self.goster('Exit')
        quit_program=True
        sys.exit(0)

    def klik2(self):
        if self.enable_display:
            self.enable_display=False
            self.pushButton_2.setText("Enable Display")
        else:
            self.enable_display=True
            self.pushButton_2.setText("Disable Display")

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

class slvModules(modbusmaslib.slvDevice):
    def __init__(self,adresxx):
        super().__init__(adresxx)

def mainLoop():
    dtonceki=0
    loopPeriod=0.1 #sn.
    msgInterval=0.01 #sn.
    global quit_program
    global port_selected

    def func3g(slvD,a,d):   #Read n words: function 3
        #print('***************')
        mesaj='Query>>> func:3(read n words) devAddr: {}  dataAddr: {}  nr of data: {}'.format(slvD.mdbsAdress,a,d)
        ui.goster(mesaj)
        response=slvD.func3(slvD.mdbsAdress,a,d)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response
    def func6g(slvD,address,data): #write a word
        mesaj='Query>>> func:6(write a word) devAddr: {}  dataAddr: {}  data: {}'.format(slvD.mdbsAdress,address,data)
        ui.goster(mesaj)
        response=slvD.func6(slvD.mdbsAdress,address,data)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response
    def func8g(slvD,subfunccode): #diagnostic
        mesaj='Query>>> func:8(diagnostic) devAddr: {}  sub func: {}  '.format(slvD.mdbsAdress,subfunccode)
        ui.goster(mesaj)
        response=slvD.func8(slvD.mdbsAdress,subfunccode)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response
    def func16g(slvD,dataaddress,datalist): #Write n consecutive words: function 16
        mesaj='Query>>> func:16(Write n consecutive words) devAddr: {}  dataAddr: {}  datalist: {}  '.format(slvD.mdbsAdress,dataaddress,datalist)
        ui.goster(mesaj)
        response=slvD.func16(slvD.mdbsAdress,dataaddress,datalist)
        mesaj='           Response : [{}]'.format(', '.join(hex(x) for x in response))
        ui.goster(mesaj)
        return response

    dtonceki=datetime.timestamp(datetime.now())
    while (not quit_program):
        if port_selected:
            for slvDev in slvArray:
                try:
                    #followings are sample messages
                    #Type here messages you want to send
                    t1=func3g(slvDev,10,5)
                    t2=func3g(slvDev,10,2)
                    t61=func6g(slvDev,20,30)
                    t81=func8g(slvDev,0)
                    t161=func16g(slvDev,50,[256,257,258])
                except modbusmaslib.NoResponseError:
                    mesaj=' error at address {} no response ...'.format(slvDev.mdbsAdress)
                    ui.goster(mesaj)
                except modbusmaslib.InvalidResponseError:
                    print ('modbuslib.InvalidResponseError:  error...')
                except modbusmaslib.comPortError:
                    print('modbusmaslib.comPortError    error...')
                    port_selected=False
                    ui.portSelectBox.setEnabled(True)
                    serial_ports()
                    ui.setportlist()
                ui.goster('scan time(sec):'+str(round(datetime.timestamp(datetime.now())-dtonceki,2)))
                dtonceki=datetime.timestamp(datetime.now())
        else:
            if not 'prevList' in locals():
                prevList=[]
            serial_ports()
            if set(serial_port_list)!=set(prevList):
                ui.setportlist()
            prevList=serial_port_list.copy()

def serial_ports():
    global serial_port_list 
    global serial_hwid_list
    #*****  Lists serial port names  *****
    ports = serial.tools.list_ports.comports()
    serial_port_list = []
    serial_hwid_list=[]
    for port, desc, hwid in sorted(ports):
        serial_port_list.append(port)
        serial_hwid_list.append(hwid)
 
if __name__ == "__main__":
    import sys
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
    # add here your modbus devices
    slvArray.append(slvModules(1))
    slvArray.append(slvModules(2))
    slvArray.append(slvModules(3))

    for indks in range(len(serial_hwid_list)):   
        if default_serial_port_loc in serial_hwid_list[indks]:
            selected_port=serial_port_list[indks]
            print(selected_port,' Selected..')
            port_selected=True
            ui.portSelectBox.setEnabled(False)
            myserialPort = serial.Serial(selected_port, baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,timeout=1)
            for x in slvArray:
                x.serialObj=myserialPort

    dongu=threading.Thread(target=mainLoop)
    dongu.start()
    sys.exit(app.exec_())