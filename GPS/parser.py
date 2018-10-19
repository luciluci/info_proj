HEADER = '''
<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.0">
<name>Sample</name>
<trk>
    <trkseg>
'''

FOOTER = '''
    </trkseg>
</trk>
</gpx>
'''

TRKPT = '''
<trkpt lat="{}" lon="{}">
    <time>{}</time>
</trkpt>
'''

VALID_FIX_TYPES = ['2D_FIX', '3D_FIX']
SIGNAL_TRESHOLD = 40

def read_data(filename):
    
    trkpts = []
    
    print (filename)
    f = open(filename, 'r')
    for line in f:
        if len(line) > 1 :#no blank lines
            items = line.split(',')
            
            if len(items) != 5:
                print ('line {} is invalid, not enought elements'.format(line))
                continue
            
            if items[2].strip() not in VALID_FIX_TYPES:
                print ('line {} is invalid, NO_FIX fix type'.format(line))
                continue
            
            if int(items[3].strip()) < SIGNAL_TRESHOLD:
                print ('line {} is invalid, low GPS signal'.format(line))
                continue
            
            trkpt = TRKPT.format(items[0].strip(), items[1].strip(), items[4].strip())
            trkpts.append(trkpt)
    f.close()
    
    return trkpts
            
def create_gpx(items, filename = 'output.gpx'):
    f = open(filename, 'w')
    f.write(HEADER)
    for item in items:
        f.write(item)
    f.write(FOOTER)
    f.close()

def main():
    trkpts = read_data('coords.txt')
    [print(item) for item in trkpts]
    create_gpx(trkpts, 'out.gpx')
    
if __name__ == '__main__':
    main()

