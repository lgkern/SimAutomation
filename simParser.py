from optparse import OptionParser
import os
import json

def parse(filename):
    ret = filename + '\n'
    ret += 'actor\tDD\tDPS\tint\thaste\tcrit\tmastery\tvers\n' 
    with open(filename, "r") as f:
        s = f.read()
        sim = json.loads(s)
        for player in sim['sim']['players']:
            if 'Int' in player['scale_factors']:
                ret+= player['name'] + '\t'
                ret+= '{0:.{1}f}'.format(player['collected_data']['dmg']['mean'],2) + '\t'
                ret+= '{0:.{1}f}'.format(player['collected_data']['dps']['mean'],2) + '\t'
                weights = player['scale_factors']
                ret+= '{0:.{1}f}'.format(weights['Int'],2) + '\t'
                ret+= '{0:.{1}f}'.format(weights['Haste'],2) + '\t'
                ret+= '{0:.{1}f}'.format(weights['Crit'],2) + '\t'
                ret+= '{0:.{1}f}'.format(weights['Mastery'],2) + '\t'
                ret+= '{0:.{1}f}'.format(weights['Vers'],2)
                ret+= '\n'
    return ret+'\n'

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-d", "--directory", dest="directory", default = None, help="the target directory")
    parser.add_option("-p", "--prefix", dest="prefix", default = '', help="the target files prefix")
    parser.add_option("-o", "--output", dest="output", default = 'statweights.txt', help="the output file to be created. Will overwrite if the file already exists.")
    (options, args) = parser.parse_args()
    
    if options.directory != None:
        os.chdir(options.directory)
    
    parses = ''
    
    print(options.prefix)
    
    for filename in os.listdir(os.getcwd()):
        if filename.startswith(options.prefix) and filename.endswith('.json'):
            parses += parse(filename)
            
    with open(options.output, "w") as ofile:
        print(parses, file=ofile)

if __name__ == "__main__":
    main()
