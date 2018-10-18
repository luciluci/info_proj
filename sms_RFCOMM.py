import dbus
import bluetooth
from guizero import App, PushButton, ListBox, Combo, Text
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
from pprint import pformat
import time

from threading import Thread

BUS_NAME='org.bluez.obex'
PATH = '/org/bluez/obex'
CLIENT_INTERFACE = 'org.bluez.obex.Client1'
SESSION_INTERFACE = 'org.bluez.obex.Session1'
MESSAGE_ACCESS_INTERFACE = 'org.bluez.obex.MessageAccess1'

OUTBOX_PATH = 'telecom/msg/outbox'

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
    
    #show available services
    #user Dial up service and get port
    #use port to create connection
    print ('connecting to {}'.format(map_devices[sel]))
    
    get_available_services(map_devices[sel])
    
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # '04:B1:67:1F:44:67'
    #sockfd.connect(map_devices[sel])
    sockfd.connect((map_devices[sel], 3))
    sockfd.send('ATZ\r')
    sockfd.send('AT+CMGF=1\r')
    sockfd.send('AT+CMGS="+40745757086"\r')
    sockfd.send('I love manele noi 2018\r')
    sockfd.send('chr(28)\r')
    sockfd.close()
    
def choose_service(sel):
    global services
    service = [service for service in services if service['name']==sel]
    current_srv = service[0]
    print (current_srv)
    
    
    #print (map_services[sel])
    print ('connecting to {} on port {}'.format(current_srv['host'], current_srv['port']))
    
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    
    sockfd.connect((current_srv['host'], current_srv['port']))
    sockfd.send('ATZ\r')
    sockfd.send('AT+CMGF=1\r')
    sockfd.send('AT+CMGS="+40745757086"\r')
    sockfd.send('I love manele noi 2018\r')
    sockfd.send('chr(28)\r')
    sockfd.close()

#callbacksCLIENT_INTERFACE
def bt_choose(sel):
    global session
    global map
    print (sel)
    
    print("Creating Session")
    
    bus = dbus.SessionBus()
    
    client = dbus.Interface(bus.get_object(BUS_NAME, PATH), CLIENT_INTERFACE)
    print ('connecting to {}'.format(map_devices[sel]))
    path = client.CreateSession(map_devices[sel], { "Target": "map" })

    obj = bus.get_object(BUS_NAME, path)
    session = dbus.Interface(obj, SESSION_INTERFACE)
    map = dbus.Interface(obj, MESSAGE_ACCESS_INTERFACE)
    time.sleep(1)
    if not map:
        print ('WARNING:no map instance available')
        return
    with open('bmessage1') as f:
        content = f.readline()
        print (content)    
    #print ('push message')
    #map.PushMessage(TEST_MSG, "telecom/msg/outbox", dict(), reply_handler=create_transfer_reply, error_handler=error)

def discover_dev():
    global map_devices
    combo.clear()
    devices = bluetooth.discover_devices(lookup_names = True)
    print ('devices found', len(devices))

    for addr, name in devices:
        map_devices[name] = addr
        combo.append(name)

if __name__ == '__main__':
    print ('ds')
    #bus = dbus.SessionBus()
    mainloop = GObject.MainLoop()
    
        
    app = App(layout="grid",bg="white",title="Bluetooth Player",width = 490,height = 300)
    combo = Combo(app, grid = [2,1], options=[], command=select_device)
    combo_sel_service = Combo(app, grid = [3,1], options=[], command=choose_service)
    
    PushButton(app,grid = [0,1], command=discover_dev, text='discover')

    tDBus = Thread(target=mainloop.run)
    tDBus.start()
