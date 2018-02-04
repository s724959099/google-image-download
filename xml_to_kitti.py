import xml.etree.cElementTree as ET
import pathlib


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    tree = ElementTree.parse('your_file.xml')
    root = tree.getroot()
    xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    root = ElementTree.XML(xml_string)
    xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))

                if self.get(element.tag):
                    if not isinstance(self.get(element.tag), list):
                        self[element.tag] = [self[element.tag]]
                    self[element.tag].append(aDict)
                else:
                    self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


def xml_to_dict(p):
    tree = ET.parse(p)
    root = tree.getroot()
    xmldict = XmlDictConfig(root)
    return xmldict


def dict_get_bbox(d):
    bbox = d['bndbox']
    return [bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']]


def txt_template(bbox):
    result = " ".join(bbox)
    return "default 0 0 0 {} 0 0 0 0 0 0 0".format(result)


def write_to_file(arr_bbox):
    if not isinstance(arr_bbox,list):
        arr_bbox = [arr_bbox]
    text = ""
    for d in arr_bbox:
        text += txt_template(dict_get_bbox(d)) + "\n"
    return text


if __name__ == '__main__':

    p = pathlib.Path("resize")
    for item in list(p.glob("*.xml")):
        d = xml_to_dict(str(item))
        txt_name = str(item).replace(".xml", ".txt")
        result = write_to_file(d['object'])
        with open(txt_name, 'w') as f:
            f.write(result)

    print("finish")
