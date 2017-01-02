def parseline(line):
    cells = line.split(',')
    return 'copy=%s\ntalents=%s\n' % (cells[6], cells[0])

output = ''
with open('talents.csv', 'r') as f:
    for line in f.readlines():
        output += parseline(line)

with open('copy_talents.simc', 'w') as o:
    o.write(output)