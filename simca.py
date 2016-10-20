import sys
from optparse import OptionParser
from subprocess import call

def sim(profile, fight, iterations=10000, scaleFactors=0, time=300, variance=0.1, bossCount=1, cores=4, outputFile=None, logFile=None):
    print("simming!")
    call("simc.exe iterations={0} calculate_scale_factors={1} max_time={2} vary_combat_length={3} fight_style={4} desired_targets={5} threads={6} html={7}.html {8}".format(iterations, scaleFactors, time, variance, fight, bossCount, cores, outputFile, profile))
    
def fight_reader(fight):
    fight = fight.lower()
    if fight in ('pw', 'patch_werk', 'patchwerk'):
        return 'Patchwerk'
    if fight in ('lm', 'light_movement', 'lightmovement'):
        return 'LightMovement'
    if fight in ('hm', 'heavy_movement', 'heavymovement'):
        return 'HeavyMovement'
    if fight in ('hs', 'helter_skelter', 'helterskelter'):
        return 'HelterSkelter'
    if fight in ('ultra', 'ux', 'ultraxion'):
        return 'Ultraxion'
    if fight in ('bl', 'beast_lord', 'beastlord'):
        return 'Beastlord'
    if fight in ('hac', 'hectic', 'hecticaddcleave'):
        return 'HecticAddCleave'
    return 'Invalid'

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--profile", dest="profilename",
                      help="sim profile file to be read (supports comma-separated lists)")
    parser.add_option("-i", "--iterations", dest="iterations",
                      help="amount of iterations to be run by each profile", default=10000)
    parser.add_option("-s", "--scale-factors", action="store_true", dest="scaleFactors",
                      help="calculate scale factors for each simulation ran", default=False)
    parser.add_option("-t", "--time", dest="time",
                      help="maximum simulation length (supports comma-separated lists)", default=300)         
    parser.add_option("-v", "--variance", dest="variance",
                      help="simulation length variance", default=0.1)    
    parser.add_option("-f", "--fights", dest="fights", default="pw"
                      help="fight styles to be simulated (supports comma-separated lists)") 
    parser.add_option("-b", "--bosses", dest="bosses",
                      help="amount of bosses in each simulation (supports comma-separated lists)", default=1)  
    parser.add_option("-c", "--cores", dest="cores",
                      help="amount of threads to be used by SimulationCraft",default=4)   
    parser.add_option("-o", "--output", dest="outputFile",
                      help="output file name (base output file name for multiple simulations)", default=None) 
    parser.add_option("-l", "--log", dest="logFile",
                      help="log file name (base log file name for multiple simulations)", default=None)   
    (options, args) = parser.parse_args()

    for time in options.time.split(","):
        for profile in options.profilename.split(","):
            for fight in options.fights.split(","):
                if isinstance(options.bosses,str):
                    for bossCount in options.bosses.split(","):
                        sim(profile, fight_reader(fight), options.iterations, 1 if options.scaleFactors else 0, time, options.variance, bossCount, options.cores, options.outputFile+profile+fight+bossCount, options.logFile)
                else:
                    sim(profile, fight_reader(fight), options.iterations, 1 if options.scaleFactors else 0, time, options.variance, options.bosses, options.cores, options.outputFile+profile+fight, options.logFile)

if __name__ == "__main__":
    main()
