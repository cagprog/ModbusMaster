This project is easy modbus library and sample application.
Developed and tested in linux system with USB-RS485 converter.

In linux following line may be required to enable USB serial port:
    sudo chmod a+rw /dev/ttyUSBx

You have to have installed required modules shown in *.py files.
To run codes place following files into same directory:

-modbusmaslib.py (Modbus RTU library)
-modbusMaster.py (Modbus RTU sample application)
-pk.py (Graphical user interface)

Then type 
python modbusMaster.py

In linux ,if there is more than one USB serial port, the same phsycal USB port may have different name (sometimes ttyUSB0 ,sometimes ttyUSB1).So code has been written to select serial port by its phsycal location.

in modbusMaster.py default_serial_port_loc variables defines serial port location.
If default_serial_port_loc is not representing a valid location, serial port location will be asked on graphical interface.