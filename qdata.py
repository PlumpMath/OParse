import sys
import os
import struct

#read the header and file length
try:
	file = open(sys.argv[1] + '/InterOp/QMetricsOut.bin', 'r')
except IOError:
	print '/InterOp/QMetricsOut.bin not found...'
	sys.exit()

print 'File version', struct.unpack('B', file.read(1))[0]
print 'Record size', struct.unpack('B', file.read(1))[0]
file.seek(0, 2)
length = file.tell() - 2
print 'Length', length
file.seek(2, 0)

#output all data
output_dir = sys.argv[1] + '/InterOp/Text/'
output_path = sys.argv[1] + '/InterOp/Text/QMetricsOut.txt'
if not os.path.exists(output_dir):
	os.makedirs(output_dir)

with open(output_path, 'w') as outfile:
	i = 0
	print >> outfile, ','.join(['Lane', 'Tile', 'Cycle'] + ['Q%s' %a for a in range(1, 51)])
	while True:
		lane = struct.unpack('H', file.read(2))[0] #Lane
		tile = struct.unpack('H', file.read(2))[0] #Tile
		cycle = struct.unpack('H', file.read(2))[0] #Cycle
		a = [lane, tile, cycle]
		for phred in range(1,51):
			a.append(struct.unpack('I', file.read(4))[0])
		print >>outfile, ','.join([str(b) for b in a])
		i += (206)
		if i == length:
			break
