from guizero import App, PushButton, ListBox, Combo, Text
import dbus
import bluetooth

#discovering BT devices

#bus = dbus.SystemBus()
#hal_manager_object =  bus.get_object('org.bluez', '/org/bluez/hci1/dev_48_13_7E_BC_48_A4')
#hal_manager_media_interface = dbus.Interface(hal_manager_object, 'org.bluez.MediaControl1')

app = App(layout="grid",bg="white",title="Bluetooth Player",width = 490,height = 300)

result = Text(app, grid=[0,0])
result.value = ''

map_devices = {}
hal_manager_media_interface = None
sms_interface = None

def play():
    print (hal_manager_media_interface)
    hal_manager_media_interface.Play()  
def pause():
    hal_manager_media_interface.Pause() 
def next_song():
    hal_manager_media_interface.FastForward() 
def previous_song():
    hal_manager_media_interface.Previous()
def volume_up():
    print (hal_manager_media_interface)
    hal_manager_media_interface.VolumeUp() 
def volume_down():
    print (hal_manager_media_interface)
    hal_manager_media_interface.VolumeDown()
def send_sms():
    print (hal_manager_media_interface)
    hal_manager_media_interface.VolumeUp() 
    
def bt_choose(sel):
    global hal_manager_media_interface
    bus = dbus.SystemBus()
    bluez_addr = map_devices[sel]
    #print (bluez_addr)
    #hal_manager_object =  bus.get_object('org.bluez', '/org/bluez/hci1/dev_48_13_7E_BC_48_A4')
    hal_manager_object =  bus.get_object('org.bluez', bluez_addr)
    hal_manager_media_interface = dbus.Interface(hal_manager_object, 'org.bluez.MediaControl1')
    print (hal_manager_media_interface)
    if hal_manager_media_interface:
        [button.enable() for button in buttons]
    #create sms interface
    #global sms_interface
    #sms_object =  bus.get_object('org.bluez.obex', '/org/bluez/obex/dev_48_13_7E_BC_48_A4')
    #sms_interface = dbus.Interface(sms_object, 'org.bluez.obex.MessageAccess1')
        
    
def generate_bluez_device_id(addr):
    bluez_addr_prefix = '/org/bluez/hci0/dev_'
    addr = addr.replace(':', '_')
    return bluez_addr_prefix + addr

def discover_dev():
    combo.clear()
    result.value = 'Discovering paired devices...'
    devices = bluetooth.discover_devices(lookup_names = True)
    result.value = ''
    for addr, name in devices:
        map_devices[name] = generate_bluez_device_id(addr)
        combo.append(name)
        #print (name, mainloop = GObject.MainLoop()addr)
        #print (generate_bluez_device_id(addr))
    return map_devices

PushButton(app,grid = [0,1], command=discover_dev, text='discover')

buttons = []
btn_play = PushButton(app,grid = [5,2],image = "resources/play.png",command=play)
btn_pause = PushButton(app,grid = [7,2],image = "resources/pause.png", command=pause)
btn_fw = PushButton(app,grid = [9,2],image = "resources/forwards.png",command=next_song)
btn_prev = PushButton(app,grid = [2,2],image = "resources/previous.png",command=previous_song)
btn_vup = PushButton(app, grid = [11,2],image = "resources/volume-up.png",command=volume_up)
btn_vdown = PushButton(app, grid = [13,2],image = "resources/volume-down.png",command=volume_down)
btn_send_sms = PushButton(app, grid=[1,3], command=send_sms)
buttons.append(btn_play)
buttons.append(btn_pause)
buttons.append(btn_fw)
buttons.append(btn_vup)
buttons.append(btn_vdown)
buttons.append(btn_prev)
for btn in buttons:
    btn.disable()

#names = [device for device in discovered_devices]
#print (names)
combo = Combo(app, grid = [2,1], options=[], command=bt_choose)


app.display()
