import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1] + '/RunInfo.xml')
root = tree.getroot()
fileout = open('RunInfo_summary.txt', 'w')

print >>fileout, 'Number,Read length'
for each in root.iter('Read'):
	print >>fileout, '%i,%i' %(int(each.attrib['Number']), int(each.attrib['NumCycles']))
