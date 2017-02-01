from os import path
from os import makedirs
import os
from optparse import OptionParser

def distribution_generator(budget, step, minStats, maxStats):
    nC,nH,nM,nV = minStats.split(',')
    xC,xH,xM,xV = maxStats.split(',')
    
    results = list()
    
    cC,cH,cM,cV = [budget,0,0,0]
    
    while cC >= 0:
        cH = budget - cC
        while cH >= 0:
            cM = budget - cC - cH
            while cM >= 0:
                cV = budget - cC - cH -cM
                if int(nC) <= cC <= int(xC) and int(nH) <= cH <= int(xH) and int(nM) <= cM <= int(xM) and int(nV) <= cV <= int(xV):
                    results.append([cC,cH,cM,cV])
                cM = cM - step
            cH = cH - step
        cC = cC - step
        
    
    return results
    
def generate_profile(combination):
    crit,haste,mast,vers=combination
    
    profile = '\ncopy='+str(crit)+'_'+str(haste)+'_'+str(mast)+'_'+str(vers)
    profile+= '\ngear_crit_rating='+str(crit)
    profile+= '\ngear_haste_rating='+str(haste)
    profile+= '\ngear_mastery_rating='+str(mast)
    profile+= '\ngear_versatility_rating='+str(vers)+'\n'
    
    return profile
   
def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="output", help="output file name", default=None) 
    parser.add_option("-d", "--directory", dest="directory", help="output directory, default is 'Distributions'", default='Distributions') 
    parser.add_option("-b", "--budget", dest="budget", help="total budget amount, the sum of ", default=None) 
    parser.add_option("-s", "--step", dest="step", help="the step between each stat variance", default=None) 
    parser.add_option("-n", "--min-stats", dest="minStats", help="minimum value for each stat in the format c,h,m,v. Please always inform all stats.", default=None)
    parser.add_option("-x", "--max-stats", dest="maxStats", help="maximum value for each stat in the format c,h,m,v. Please always inform all stats.", default=None)
    parser.add_option("-z", "--debug", action="store_true", dest="debug", help="prints out the combinations of stats that would be generated. Doesn't create the file", default=False)
    
    (options, args) = parser.parse_args()
    
    if not options.output:
        print('Error: Please inform the output file name.')
        return
    
    if not options.budget:
        print('Error: Please inform the total stat budget.')
        return
        
    if not options.step:
        print('Error: Please inform the step between each stat variance')
        return
    
    if not options.minStats:
        print('Error: Please inform the minimum value of all stats')
        return
        
    if not options.maxStats:
        print('Error: Please inform the maximum value of all stats')
        return
        
    if len(options.minStats.split(',')) != 4 or len(options.maxStats.split(',')) != 4:
        print('Error: Please inform exactly 4 values for min and max values.')
        return
        
    combinations = distribution_generator(int(options.budget), int(options.step), options.minStats, options.maxStats)
    
    if options.debug:
        print(combinations)
        return
    
    result = ''
    
    for combination in combinations:
        result += generate_profile(combination)
        
    if not path.exists(options.directory):
        makedirs(options.directory)
    
    if options.directory != None:
        os.chdir(options.directory)
    
    with open(options.output, "w") as ofile:
        print(result, file=ofile)
        
if __name__ == "__main__":
    main()