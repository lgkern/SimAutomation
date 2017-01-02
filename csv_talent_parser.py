def parseline(line, talent):
    cells = line.split(',')
    if(cells[5] == talent):
        return 'copy=%stalents=%s\n\n' % (cells[6], cells[0])
    return ''

output = ''
with open('talents.csv', 'r') as f:
    for line in f.readlines():
        output += parseline(line,'S2M')
with open('copy_talents_1.simc', 'w') as o:
    o.write(output)
output = ''    
with open('talents.csv', 'r') as f:
    for line in f.readlines():
        output += parseline(line,'SC')
    with open('copy_talents_2.simc', 'w') as o:
        o.write(output)
output = ''
with open('talents.csv', 'r') as f:
    for line in f.readlines():
        output += parseline(line,'LotV')
    with open('copy_talents_3.simc', 'w') as o:
        o.write(output)