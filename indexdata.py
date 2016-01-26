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
file.seek(0, 2)
length = file.tell() - 1
print 'Length', length
file.seek(1, 0)

#output all data
fname_tiles = 'IndexMetricsOut_tiles.txt'
with open(fname_tiles, 'w') as tiles:
	print >>tiles, ','.join(['Tile', 'Swath', 'Tile', 'Bool1', 'Bool2', 'Index1', 'Index2', 'Read count', 'Sample name', 'Project name'])
	i = 0
	while True:
		lane = struct.unpack('B', file.read(1))[0] #Lane
		swath = struct.unpack('B', file.read(1))[0] #Swath
		tile = struct.unpack('H', file.read(2))[0] #Tile
		bool1 = struct.unpack('?', file.read(1))[0] #?
		bool2 = struct.unpack('?', file.read(1))[0] #?
		indexlen = struct.unpack('H', file.read(2))[0]
		index1, index2 = struct.unpack('%ss' %(indexlen), file.read(indexlen))[0].split('-')
		readcount = struct.unpack('i', file.read(4))[0]
		samplelen = struct.unpack('H', file.read(2))[0]
		sample = struct.unpack('%ss' %(samplelen), file.read(samplelen))[0]
		projectlen = struct.unpack('H', file.read(2))[0]
		project = struct.unpack('%ss' %(projectlen), file.read(projectlen))[0]
		print >>tiles, '%i,%i,%i,%s,%s,%s,%s,%i,%s,%s' %(lane, swath, tile, bool1, bool2, index1, index2, readcount, sample, project)
		i += (16 + indexlen + samplelen + projectlen)
		if i == length:
			break
