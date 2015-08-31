import fastkml
from coord_utils import CoordUtils
from fastkml.config import etree

class StreetList:
    streets_dir = ''
    kml = ''
    itemsGen = ''

    def __init__(self,streets_dir):
        self.streets_dir = streets_dir
        self.load_streets_kml()
        pass

    def load_streets_kml(self):
        with open('{}/streets.kml'.format(self.streets_dir)) as data_file:
            self.kml = fastkml.KML()
            self.kml.from_string(data_file.read())
            features = list(self.kml.features())
            self.itemsGen = list(features)[0].features()

    def __iter__(self):
        return self

    def next(self):
        item_dict = {
                'id': '',
                'kml_id': '',
                'bounds': '',
                'street_name': '',
                'borough_code': '',
                'zip_code': ''}
        item = self.itemsGen.next()
        try:
            item_dict['kml_id'] = item.name
            item_dict['bounds'] = item.geometry.bounds
            et = etree.fromstring('<root>'+item.description+'</root>')
            for li in et.findall('ul/li'):
                atrname = li.find(".//*[@class='atr-name']")
                if (atrname is not None):
                    atrval = li.find(".//*[@class='atr-value']")
                    if (atrname.text == "PHYSICALID"):
                        item_dict['id'] = atrval.text
                    elif (atrname.text == "STNAME_LAB"):
                        item_dict['street_name'] = atrval.text
                    elif (atrname.text == "BOROUGHCOD"):
                        item_dict['borough_code'] = atrval.text
                    elif (atrname.text == "L_ZIP"):
                        item_dict['zip_code'] = atrval.text
        except Exception:
            pass
        return item_dict
