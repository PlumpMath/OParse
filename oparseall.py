import os
import re
import sys
import xml.etree.ElementTree as et
import twitter
import tiledata
import indexdata
from settings import ts, machines, base_path, run_pattern

def tweet(message, users):
        t = twitter.Twitter(auth=twitter.OAuth(ts['token'], ts['token_key'], ts['con_secret_key'], ts['con_secret']))
        for u in users:
                t.direct_messages.new(user=u, text=message)
                print 'Sent direct message to %s' % (u)

def id_dirs_to_parse(machine, run_pattern, overwrite=False):
    # Regex, list sequencing dir paths
    machine_path = base_path + machine + '/'
    candidate_dirs = [machine_path + d for d in os.listdir(machine_path) if re.search(r'^\d{6}_[A-Z]\d{5}_\d{4}.*$', d)]
    
    # Use read/cycles pattern to identify runs
    matching_dirs = []
    for d in candidate_dirs:
        if os.path.isfile(d + '/RTAComplete.txt'):
            if overwrite or not os.path.isfile(d + '/InterOp/Text/TileMetricsOut.txt'):
                try:
                    tree = et.parse(d + '/RunInfo.xml')
                    root = tree.getroot()
                    read_cycles = []
                    for each in root.iter('Read'):
                        read = int(each.attrib['Number'])
                        cycles = int(each.attrib['NumCycles'])
                        read_cycles.append((read, cycles))
                    read_cycles = tuple(read_cycles)
                    if read_cycles == run_pattern:
                        matching_dirs.append(d)
                except IOError:
                    print '%s is not a sequencing folder (no RunInfo.xml)' % (d)
                except:
                    print 'Unexpected error: ', sys.exc_info()
            else:
                print 'Skip ' + d + ': Not new'
    return matching_dirs
    
def main():
    # Get all target dirs
    target_dirs = []
    for m in machines:
        for d in id_dirs_to_parse(m, run_pattern, overwrite=True):
            target_dirs.append(d)
    
    # Parse targets
    for t in target_dirs:
        tiledata.parse_tile_metrics(t)
        indexdata.parse_index_data(t)
        #tweet('Parsed new sequencing run data for ' + t, ts['dm_users'])
        # TODO: SLACK API
    
if __name__ == '__main__':
    main()