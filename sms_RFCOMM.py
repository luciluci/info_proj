import bluetooth
from guizero import App, PushButton, ListBox, Combo, Text

session = None
map = None
map_devices = {}
services = None
    
def get_available_services(device_addr):
    global services
    print ('detecting services for {}'.format(device_addr))
    services = bluetooth.find_service(address=device_addr)
    combo_sel_service.clear()
    for svr in services:
        if svr['name']:
            combo_sel_service.append(svr['name'])
        print ('name: {} '.format(svr))
        
def select_device(sel):
    print ('selected device {}'.format(map_devices[sel]))
    get_available_services(map_devices[sel])

    
def choose_service(sel):
    global services
    service = [service for service in services if service['name']==sel]
    current_srv = service[0]
    print (current_srv)
        
    print ('2connecting to {} on port {}'.format(current_srv['host'], current_srv['port']))
    
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    
    s.connect((current_srv['host'], current_srv['port']))
        
    s.send("AT\r")
    print (s.recv(1024))

    s.send("AT+CMGF=1\r")
    print (s.recv(1024))

    s.send('AT+CMGS="0745757086"\r')
    print (s.recv(1024))
    s.send("This is freds test!"+chr(26))
    print (s.recv(1024))
    print (s.recv(1024))
    
    s.close()

def discover_dev():
    global map_devices
    combo.clear()
    devices = bluetooth.discover_devices(lookup_names = True)
    print ('devices found', len(devices))

    for addr, name in devices:
        map_devices[name] = addr
        combo.append(name)

if __name__ == '__main__':    
        
    app = App(layout="grid",bg="white",title="Bluetooth Player",width = 490,height = 300)
    combo = Combo(app, grid = [2,1], options=[], command=select_device)
    combo_sel_service = Combo(app, grid = [3,1], options=[], command=choose_service)
    
    PushButton(app,grid = [0,1], command=discover_dev, text='discover')

