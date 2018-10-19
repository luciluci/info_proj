HEADER_GPX = '''
<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.0">
<name>Sample</name>
<trk>
    <trkseg>
'''

FOOTER_GPX = '''
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

HEADER_KML = '''
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Paths</name>
            <description>Examples of paths</description>   
                <Style id="linestyleExample">
                    <LineStyle>
                        <color>FFB42814</color>
                        <width>4</width>                            
                    </LineStyle>
                </Style>
                <Placemark>
                    <name>Example placemark</name>     
                    <styleUrl>#linestyleExample</styleUrl>                                          
                <LineString>
                    <coordinates>
'''

FOOTER_KML = '''</coordinates>
            </LineString>
        </Placemark>
    </Document>
</kml>
'''

COORDINATE = '''
{}, {}
'''


def read_data(filename):
    
    points = []
    
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
            
            point = [items[0].strip(), items[1].strip(), items[4].strip()]
            points.append(point)
    f.close()
    
    return points
            
def create_gpx(items, filename = 'output.gpx'):
    f = open(filename, 'w')
    f.write(HEADER_GPX)
    for item in items:
        trkpt = TRKPT.format(item[0], item[1], item[2])
        f.write(trkpt)
    f.write(FOOTER_GPX)
    f.close()
    
def create_kml(items, filename = 'output.kml'):
    f = open(filename, 'w')
    f.write(HEADER_KML)
    for item in items:
        coord = COORDINATE.format(item[0], item[1])
        f.write(coord)
    f.write(FOOTER_KML)
    f.close()

def main():
    points = read_data('coords.txt')
    [print(item) for item in points]
    create_gpx(points, 'out.gpx')
    create_kml(points, 'out.kml')
    
    
if __name__ == '__main__':
    main()

