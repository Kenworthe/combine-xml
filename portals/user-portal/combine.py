'''
Looks for a template.xml (header-and-footer.xml),
and then inserts contents of all .xml files in current 
directory into the <screens></screens> tags in template.xml
and then outputs the combined file into /output/final.xml.
'''

from xml.etree import ElementTree
from xml.dom import minidom
import os, sys
import glob

def combine():

    # TODO: Investigate if all these paths are necessary. Easy way is to dumb combine files.
    # TODO: Investigate why script will randomly fail. Probably due to (async?) chdir.

    script_path = os.path.dirname(os.path.realpath(__file__))
    screens_path = script_path + '/screens'
    template_path = script_path + '/template'
    output_path = script_path + '/output'

    os.chdir(template_path)
    template = glob.glob('*.xml')[0]  # TODO: Specifically look for 'template.xml' instead of [0]
    template_data = ElementTree.parse(template).getroot()
    print ElementTree.tostring(template_data)

    os.chdir(screens_path)
    screens = glob.glob('*.xml')

    output_xml = None


    # Below combines the xmls, but only under root "<Screen>"
    # TODO: Find way to make it keep all individual Screen tags 
    # TODO: INSERT all <Screen> files into <Screens> tag in template.xml

    for screen in screens:
        data = ElementTree.parse(screen).getroot()
        # print ElementTree.tostring(data)

        if output_xml is None:
            output_xml = data
        else:
            output_xml.extend(data)

    # Prettify the xml doc before adding to final xml
    strip(output_xml)
    pretty_output = minidom.parseString(ElementTree.tostring(output_xml)).toprettyxml(indent="  ", newl="\n")

    final = open(output_path + '/user-portal-final.xml', 'w')
    final.write(pretty_output)

# Used for prettifying xml
def strip(elem):
    for elem in elem.iter():
        if(elem.text):
            elem.text = elem.text.strip()
        if(elem.tail):
            elem.tail = elem.tail.strip()


combine()


# METHOD 1: 

# xml_files = glob.glob(files +'/*.xml')
# xml_element_tree = None
# for xml_file in xml_files:
#     data = ElementTree.parse(xml_file).getroot()
#     # print ElementTree.tostring(data)
#     for result in data.iter('results'):
#         if xml_element_tree is None:
#             xml_element_tree = data 
#             insertion_point = xml_element_tree.findall('./results')[0]
#         else:
#             insertion_point.extend(result) 
# if xml_element_tree is not None:
#     print ElementTree.tostring(xml_element_tree)



# METHOD 2: 

# def combine_xml(files):
#     first = None
#     for filename in files:
#         data = ElementTree.parse(filename).getroot()
#         if first is None:
#             first = data
#         else:
#             first.extend(data)
#     if first is not None:
#         return ElementTree.tostring(first)