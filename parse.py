import sys
import struct
import numpy

metric = {100:'Cluster density (k/mm2)', 101:'Cluster density Pf (k/mm2)', 102:'Clusters (k)', 103:'Clusters Pf (k)', 200:'Phasing R1', 201:'Prephasing R1', 202:'Phasing R2', 203:'Prephasing R2', 300:'Percent aligned R1', 301:'Percent aligned R2', 400:'Unknown'}

codes = sorted(metric.keys())

#read the header and file length
file = open(sys.argv[1])
print 'File version', struct.unpack('B', file.read(1))[0]
record_size = struct.unpack('B', file.read(1))[0]
file.seek(0, 2)
length = file.tell()
file.seek(2, 0)
records = (length-2) / record_size
print 'Records', records

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

#read the data into numpy array
data = []
for lane in lanes_sort:
	data.append(numpy.zeros((len(tiles),), dtype='i2, i2, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4'))
	for tile in tiles_sort:
		data[lane-1][tiles_sort.index(tile)][0] = 1
		data[lane-1][tiles_sort.index(tile)][1] = tile
	for record in range(records):
		a = struct.unpack('H', file.read(2))[0]
		b = struct.unpack('H', file.read(2))[0]
		c = struct.unpack('H', file.read(2))[0]
		d = struct.unpack('f', file.read(4))[0]
		data[lane-1][tiles_sort.index(b)][codes.index(c) + 2] = d

#output all data
fname_tiles = sys.argv[1].split('/')[-1].split('.')[0] + '_tiles.txt'
with open(fname_tiles, 'w') as tiles:
	header = ['Lane', 'Tile'] + [metric[code] for code in codes][:-7] + ['% Pass Filter'] + [metric[code] for code in codes][4:-1]
	print >>tiles, ','.join(header)
	for lane in data:
		for row in lane:
			print >>tiles, '%i,%i,%.1f,%.1f,%.1f,%.1f,%.1f,%.3f,%.3f,%.3f,%.3f,%.1f,%.1f' %(row[0], row[1], row[2]/1000, row[3]/1000, row[4]/1000, row[5]/1000, (row[3]/row[2])*100, row[6], row[7], row[8], row[9], row[10], row[11])

#output averages
fname_summary = sys.argv[1].split('/')[-1].split('.')[0] + '_summary.txt'
with open(fname_summary, 'w') as summary:
	header[1] = 'Tiles'
	print >>summary, ','.join(header)
	for n, lane in enumerate(data):
		print >>summary, '%i,%i,%.1f,%.1f,%.1f,%.1f,%.1f,%.3f,%.3f,%.3f,%.3f,%.1f,%.1f' %(n+1, len(set([row[1] for row in lane])), numpy.mean([row[2] for row in lane])/1000, numpy.mean([row[3] for row in lane])/1000, numpy.mean([row[4] for row in lane])/1000, numpy.mean([row[5] for row in lane])/1000,(numpy.mean([row[5] for row in lane])/numpy.mean([row[4] for row in lane]))*100, numpy.mean([row[6] for row in lane]), numpy.mean([row[7] for row in lane]), numpy.mean([row[8] for row in lane]), numpy.mean([row[9] for row in lane]), numpy.mean([row[10] for row in lane]), numpy.mean([row[11] for row in lane]))

