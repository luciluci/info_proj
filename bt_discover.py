import bluetooth
#from pybtooth import BluetoothManager

#bm = BluetoothManager()
#devices = bm.getDevices()
#print (devices)
#phone = devices[0]
#phone.Paired
#phone.Connected
#phone.Connect()
#for item in bm.getConnectedDevices():
#    print ('connected devices ' + item)
devices = bluetooth.discover_devices(lookup_names = True)

def create_bluez_device_id(addr):
    bluez_addr_prefix = '/org/bluez/hci0/dev_'
    addr = addr.replace(':', '_')
    return bluez_addr_prefix + addr

for addr, name in devices:
    print (name, addr)
    print (create_bluez_device_id(addr))
    
#'/org/bluez/hci0/dev_48_13_7E_BC_48_A4'