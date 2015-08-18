

from motionless import AddressMarker, LatLonMarker,DecoratedMap, CenterMap, VisibleMap
import xml.sax

class GPXHandler(xml.sax.handler.ContentHandler):
    def __init__(self,gmap):
        self.gmap = gmap
        self.first = True 
        self.prev = None

    def startElement(self, name, attrs):
        if name == 'trkpt': 
            self.gmap.add_path_latlon(attrs['lat'],attrs['lon'])
            self.prev = (attrs['lat'],attrs['lon'])
            if self.first:
                self.first = False
                self.gmap.add_marker(LatLonMarker(attrs['lat'],attrs['lon'],color='green',label='S'))

    def endElement(self,name):
        if name == 'trk':
            self.gmap.add_marker(LatLonMarker(self.prev[0],self.prev[1],color='red',label='E'))
        
