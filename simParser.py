from optparse import OptionParser
import os
import json
from os import path

def parse(filename, isCsv, hideHeaders):
    separator = ',' if isCsv else '\t'
    if(hideHeaders):
        ret = ''
    else:   
        ret = filename + '\n'
        ret += 'actor'+separator+'DD'+separator+'DPS'+separator+'int'+separator+'haste'+separator+'crit'+separator+'mastery'+separator+'vers\n' 
    with open(filename, "r") as f:
        s = f.read()
        sim = json.loads(s)
        for player in sim['sim']['players']:
            if 'Int' in player['scale_factors']:
                if(hideHeaders):
                    ret+= path.splitext(filename)[0]+separator
                else:
                    ret+= player['name'] + separator
                ret+= '{0:.{1}f}'.format(player['collected_data']['dmg']['mean'],2) + separator
                ret+= '{0:.{1}f}'.format(player['collected_data']['dps']['mean'],2) + separator
                weights = player['scale_factors']
                ret+= '{0:.{1}f}'.format(weights['Int'],2) + separator
                ret+= '{0:.{1}f}'.format(weights['Haste'],2) + separator
                ret+= '{0:.{1}f}'.format(weights['Crit'],2) + separator
                ret+= '{0:.{1}f}'.format(weights['Mastery'],2) + separator
                ret+= '{0:.{1}f}'.format(weights['Vers'],2)
                ret+= '\n'
    return ret+ '\n' if not hideHeaders else ret

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-d", "--directory", dest="directory", default = None, help="the target directory")
    parser.add_option("-p", "--prefix", dest="prefix", default = '', help="the target files prefix")
    parser.add_option("-o", "--output", dest="output", default = 'statweights.txt', help="the output file to be created. Will overwrite if the file already exists")
    parser.add_option("-c", "--csv",  action="store_true", dest="csv", default = False, help="Checks if the output file should be in the CSV format or TXT")
    parser.add_option("-r", "--hide-headers",  action="store_true", dest="hideHeaders", default = False, help="hides the headers from files for better sheet export")
    (options, args) = parser.parse_args()
    
    if options.directory != None:
        os.chdir(options.directory)
    
    separator = ',' if options.csv else '\t'
    
    parses = '' if not options.hideHeaders else 'actor'+separator+'DD'+separator+'DPS'+separator+'int'+separator+'haste'+separator+'crit'+separator+'mastery'+separator+'vers\n'
    
    print(options.prefix)
    
    for filename in os.listdir(os.getcwd()):
        if filename.startswith(options.prefix) and filename.endswith('.json'):
            parses += parse(filename, options.csv, options.hideHeaders)
            
    with open(options.output, "w") as ofile:
        print(parses, file=ofile)

if __name__ == "__main__":
    main()
