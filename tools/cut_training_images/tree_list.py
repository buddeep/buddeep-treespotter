import fastkml
from coord_utils import CoordUtils
from fastkml.config import etree

class TreeList:
    i = 0
    trees_dir = ''
    kml = ''
    trees = []

    def __init__(self,trees_dir):
        self.trees_dir = trees_dir
        self.load_trees_kml()
        pass

    def load_trees_kml(self):
        with open('{}/trees.kml'.format(self.trees_dir)) as data_file:
            kml = fastkml.KML()
            kml.from_string(data_file.read())
            features = list(kml.features())
            # TODO put in iterator
            self.trees = list(features[0].features())

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.trees):
            i = self.i
            self.i += 1
            tree = self.trees[i]
            tree_kml_id = tree.name.split('.')[1]
            tree_id = ''
            et = etree.fromstring('<root>'+tree.description+'</root>')
            for li in et.findall('ul/li'):
                atrname = li.find(".//*[@class='atr-name']")
                if (atrname is not None) and (atrname.text == "TREEID"):
                    atrval = li.find(".//*[@class='atr-value']")
                    tree_id = atrval.text
            tree_latlng = [tree.geometry.y,tree.geometry.x]
            return {'id': tree_id,
                'kml_id': tree_kml_id,
                'latlng': tree_latlng}
        else:
            raise StopIteration()
