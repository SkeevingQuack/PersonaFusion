import re

f = open('ugly_slugs.txt', mode='r')

fluff = []
unknown = []
proper = []

for line in f:
    groups = line.strip().split()

    if len(groups) < 2:
        fluff.append(line.strip())
    elif groups[-1].isdecimal():
        proper.append( (' '.join(groups[:-1]), groups[-1]) )
    elif groups[-1] == '?':
        unknown.append(' '.join(groups[:-1]))
    else:
        fluff.append(line.strip())

f.close()
f = open('slugs.csv', mode='w')
for pair in proper:
    f.write('"{}", "{}"\n'.format(*pair))
for name in unknown:
    f.write('"{}", "{}"\n'.format(name, '?'))
f.close()
