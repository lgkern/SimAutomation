# SimAutomation

1. Download and install the latest [Python 3.x version](https://www.python.org/downloads/)
2. [Download the tool itself](https://github.com/lgkern/SimAutomation/archive/master.zip)

When installing python make sure to check the Add to PATH option

drop the script inside SimC folder, then run 
```
python simca.py --help
```

to see the available options
a valid call:
```
python simca.py -p no_s2m.simc,s2m.simc -f pw,lm,hm,hs -b 1,2 -o batch_5
```

That will run the profiles no_s2m.simc and s2m.simc for 1 and 2 bosses for patchwerk, lightmovement, heavymovement and helterstelker and create all the result html files with the prefix batch_5

the output files names are not 100% right now, but they do their job. 

if you do 2 batches with the same -o option, they will override for the same profile, fight, boss

This command examples assume that simc.exe, simca.py and all the desired profiles are in the same folder
