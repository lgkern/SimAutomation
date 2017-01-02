from os import path
from os import chdir
from os import makedirs
from optparse import OptionParser

def create_profile(header, apl, gear, talent, boss, add):
    header_content = ''
    apl_content = ''
    gear_content = ''
    talent_content = ''
    boss_content = ''
    add_content = ''
    filename = ''
    print(header + '.' +apl + '.' +gear + '.' +talent + '.' +boss + '.' +add)
    
    if len(boss) > 0:
        with open(boss, 'r') as f:
            boss_content += f.read()
            filename += path.splitext(boss)[0] + '_'

    if len(talent) > 0:
        with open(talent, 'r') as f:
            talent_content += f.read()
            filename += path.splitext(talent)[0] + '_'
            
    if len(header) > 0:
        with open(header, 'r') as f:
            header_content += f.read()
            
    if len(gear) > 0:
        with open(gear, 'r') as f:
            gear_content += f.read()
            filename += path.splitext(gear)[0] + '_'
            
    if len(apl) > 0:
        with open(apl, 'r') as f:
            apl_content += f.read()
            
    if len(add) > 0:
        with open(add, 'r') as f:
            add_content += f.read()
            filename += path.splitext(add)[0]
    
    if not path.exists('profiles'):
        makedirs('profiles')
    
    chdir('profiles')
    
    with open(filename+'.simc', 'w') as f:
        f.write(header_content+'\n'+apl_content+'\n'+gear_content+'\n'+talent_content+'\n'+boss_content+'\n'+add_content+'\n')
        
    chdir('..')
            
def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-d", "--header", dest="header", default = '', help="header files")
    parser.add_option("-l", "--apl", dest="apl", default = '', help="APL files")
    parser.add_option("-g", "--gear", dest="gear", default = '', help="gear files")
    parser.add_option("-t", "--talents", dest="talents", default = '', help="talent files")
    parser.add_option("-b", "--bosses", dest="bosses", default = '', help="bosses files")
    parser.add_option("-a", "--adds", dest="adds", default = '', help="adds files")
    (options, args) = parser.parse_args()
    
    headers = options.header.split(',')
    apls = options.apl.split(',')
    gears = options.gear.split(',')
    talents = options.talents.split(',')
    bosses = options.bosses.split(',')
    adds = options.adds.split(',')
    
    for header in headers:
        for apl in apls:
            for gear in gears:
                for talent in talents:
                    for boss in bosses:
                        for add in adds:
                            create_profile(header, apl, gear, talent, boss, add)

    
if __name__ == "__main__":
    main()
    