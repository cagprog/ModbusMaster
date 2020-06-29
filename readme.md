This project is easy modbus library and sample application.
Developed and tested in linux system with USB-RS485 converter.
In linux following line may be required to enable USB serial port:
    sudo chmod a+rw /dev/ttyUSBx

You have to have installed required modules shown in *.py files.
To run codes place following files into same directory:

-modbusmaslib.py (Modbus RTU librart)
-modbusMaster.py (Modbus RTU sample application)
-pk.py (Graphical user interface)

Then type 
python modbusMaster.py

in modbusMaster.py default_serial_port_loc variables defines serial port location.If this variable is not matched on panel serial port location will be asked.