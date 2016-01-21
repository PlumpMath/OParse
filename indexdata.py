import sys
import struct
import numpy

#read the header and file length
try:
	file = open(sys.argv[1] + '/InterOp/IndexMetricsOut.bin', 'r')
except IOError:
	print '/InterOp/IndexMetricsOut.bin not found...'
	sys.exit()

print 'File version', struct.unpack('B', file.read(1))[0]
record_size = struct.unpack('B', file.read(1))[0]
file.seek(0, 2)
length = file.tell()
file.seek(2, 0)
records = (length-2) / record_size
print 'Records', records

"""
#get number of lanes and tiles
lanes = set([])
tiles = set([])
for record in range(records):
        lanes.update([struct.unpack('H', file.read(2))[0]])
        tiles.update([struct.unpack('H', file.read(2))[0]])
        file.read(6)
print 'Lanes', len(lanes)
print 'Tiles', len(tiles)
lanes_sort = sorted(lanes)
tiles_sort = sorted(tiles)
file.seek(2, 0)
"""

file.read(1) #0

for each in range(190):
	print struct.unpack('H', file.read(2))[0]
	file.read(4) #458754
	print struct.unpack('6s', file.read(6))[0]
        print struct.unpack('I', file.read(4))[0]
	file.read(1) #0
	strlen = struct.unpack('B', file.read(1))[0]
	file.read(1) #0
	print struct.unpack('%ss' %(strlen), file.read(strlen))[0]
	file.read(4) #65536
	
