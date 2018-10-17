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

TEST_MSG = '''BEGIN:BMSG<CR><LF>\
VERSION:1.0<CR><LF>\
STATUS:UNREAD<CR><LF>\
TYPE:SMS_GSM<CR><LF>\
FOLDER:telecom/msg/outbox<CR><LF>\
BEGIN:VCARD<CR><LF>\
VERSION:2.1<CR><LF>\
FN:Mark Jens<CR><LF>\
N:Jens, Mark<CR><LF>\
TEL:0040745754188<CR><LF>\
EMAIL:<CR><LF>\
END:VCARD<CR><LF>\
BEGIN:BENV<CR><LF>\
BEGIN:VCARD<CR><LF>\
VERSION:2.1<CR><LF>\
FN:Jens Hanssen<CR><LF>\
N:<CR><LF>\
TEL:0040745757086<CR><LF>\
EMAIL:<CR><LF>\
END:VCARD<CR><LF>\
BEGIN:BBODY<CR><LF>\
CHARSET:UTF-8<CR><LF>\
LENGTH:103<CR><LF>\
BEGIN:MSG<CR><LF>\
Bonjour, je serai en retard. Envoyé depuis ma voiture (aucune réponse attendue)<CR><LF>\
END:MSG<CR><LF>\
END:BBODY<CR><LF>\
END:BENV<CR><LF>'''


session = None
map = None
map_devices = {}

def unwrap(x):
    """Hack to unwrap D-Bus values, so that they\'re easier to read when
    printed. Taken from d-feet """

    if isinstance(x, list):
        return map(unwrap, x)

    if isinstance(x, tuple):
        return tuple(map(unwrap, x))

    if isinstance(x, dict):
        return dict([(unwrap(k), unwrap(v)) for k, v in x.items()])

    for t in [str, int, float, bool]:
        if isinstance(x, t):
            return t(x)

    return x

def dbus_loop():
    print ('starting dbus loop')
    print (dbus)
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    mainloop = GObject.MainLoop()
    mainloop.run()

#callbacksCLIENT_INTERFACE
def bt_choose(sel):
    global session
    global map
    print (sel)
    
    print("Creating Session")
    
    #tDBus = Thread(target=dbus_loop)
    #tDBus.start()
    
    bus = dbus.SessionBus()
    
    #dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    #mainloop = GObject.MainLoop()
    #tDBus = Thread(target=mainloop.run())
    
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
        #print (name, addr)
        #print (generate_bluez_device_id(addr))
    
def create_transfer_reply(path, properties):
    print ('reply')
    transfer_path = path
    props[path] = properties
    if self.verbose:
        print("Transfer created: %s (file %s)" % (path, properties["Filename"]))

def errorss(err):
    print(err)
    mainloop.quit()
    
def push_message():
    global map
    print (map)
    print ('push message:' + TEST_MSG)
    map.PushMessage(TEST_MSG, "telecom/msg/outbox", dict(), reply_handler=create_transfer_reply, error_handler=errorss)
        
def list_folders():
    global map
    print (map)
    print ('list folders')
    for i in map.ListFolders(dict()):
        print("%s/" % (i["Name"]))
        map.SetFolder(i["Name"])
        for j in map.ListFolders(dict()):
            print("    %s/" % (j["Name"]))
            map.SetFolder(j['Name'])
            for k in map.ListFolders(dict()):
                print("        %s/" % (k["Name"]))
                #if k["Name"] == 'draft':
                if k["Name"] == 'draft':
                    map.SetFolder(k['Name'])
                    print ('push message:' + TEST_MSG)
                    map.PushMessage(TEST_MSG, "", dict(), reply_handler=create_transfer_reply, error_handler=errorss)
                    #try:
                    #    print ('list messages')
                    #    ret = map.ListMessages('', dict())
                    #    print(pformat(unwrap(ret)))
                    #except dbus.exceptions.DBusException as e:
                    #    print ('ERROR: ListMessages failed' + e.get_dbus_message())
                

def list_messages():
    global map
    print (map)
    print ('list messages')
    try:
        ret = map.ListMessages('telecom/msg/draft', dict())
        print(pformat(unwrap(ret)))
    except dbus.exceptions.DBusException as e:
        print ('ERROR: ListMessages failed' + e.get_dbus_message())
    
    #print ('list messages')
    #try:
    #    ret = map.ListMessages('telecom', dict())
    #    print(pformat(unwrap(ret)))
    #except dbus.exceptions.DBusException as e:
    #    print ('ERROR: ListMessages failed' + e.get_dbus_message())
    #print ('push message')
    #map.PushMessage('bmessage1', "telecom/msg/outbox", dict(), reply_handler=create_transfer_reply, error_handler=errorss)


if __name__ == '__main__':
    print ('ds')
    #bus = dbus.SessionBus()
    mainloop = GObject.MainLoop()
    
        
    app = App(layout="grid",bg="white",title="Bluetooth Player",width = 490,height = 300)
    combo = Combo(app, grid = [2,1], options=[], command=bt_choose)
    PushButton(app,grid = [0,1], command=discover_dev, text='discover')
    btn_play = PushButton(app,grid = [1,1],command=push_message, text='send_sms')
    btn_play = PushButton(app,grid = [3,1],command=list_folders, text='list folders')
    btn_play = PushButton(app,grid = [4,1],command=list_messages, text='list messages')

    tDBus = Thread(target=mainloop.run)
    tDBus.start()
