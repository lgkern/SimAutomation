import sys
from optparse import OptionParser
from subprocess import call
from os import path

resumeMode = False
disableBloodlust = False
optimalRaid = False
scaleFactors = 0
json2 = False
scaleOnly = None

def sim(profile, fight, iterations=10000, time=300, variance=0.1, bossCount=1, cores=4, outputFile=None, logFile=None, plotStats=None, plotPoints=20, plotStep=160.0, plotTargetError=0.1, xmlFile = None, jsonFile = None):
    print("Revision 51 2017-05-11")

    arguments='iterations={0} calculate_scale_factors={1} max_time={2} vary_combat_length={3} fight_style={4} desired_targets={5} threads={6}'.format(iterations, scaleFactors, time, variance, fight, bossCount, cores)
    if disableBloodlust:
        arguments+=' override.bloodlust=0'
    if plotStats:
        arguments+=' dps_plot_stat={0} dps_plot_points={1} dps_plot_step={2}'.format(plotStats, plotPoints, plotStep)
        if plotTargetError != 0.1:
            arguments+=' dps_plot_target_error={0}'.format(plotTargetError)
    if scaleOnly:
        arguments += ' scale_only={0}'.format(scaleOnly)
    if outputFile:
        arguments+=' html={0}.html'.format(outputFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time)
    if xmlFile:
        arguments+=' xml={0}.xml'.format(xmlFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time)
    if jsonFile:
        arguments+=' json2={0}.json'.format(jsonFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time)
    arguments += ' output=nul '
    arguments+=' {0}'.format(profile)
    if logFile:
       arguments+=' > {0}.log'.format(logFile)
    hasJsonFile = resumeMode and jsonFile and path.isfile('{0}.json'.format(jsonFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time))
    hasHtmlFile = resumeMode and outputFile and path.isfile('{0}.html'.format(outputFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time))

    if hasHtmlFile:
       print('Resume Mode! Skipping {0}\n'.format(outputFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time))
    elif hasJsonFile:
       print('Resume Mode! Skipping {0}\n'.format(jsonFile+'_'+profile+'_'+fight+'_'+bossCount+'_'+time))
    else:
       call("./simc "+arguments, shell=True)

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
    parser.add_option("-p", "--profile", dest="profilename", help="sim profile file to be read (supports comma-separated lists)")
    parser.add_option("-i", "--iterations", dest="iterations", help="amount of iterations to be run by each profile", default=10000)
    parser.add_option("-s", "--scale-factors", action="store_true", dest="scaleFactors", help="calculate scale factors for each simulation ran", default=False)
    parser.add_option("-t", "--time", dest="time", help="maximum simulation length (supports comma-separated lists)", default=300)
    parser.add_option("-v", "--variance", dest="variance", help="simulation length variance, ranges from 0 to 1", default=0.1)
    parser.add_option("-f", "--fights", dest="fights", default="pw", help="fight styles to be simulated (supports comma-separated lists)")
    parser.add_option("-b", "--bosses", dest="bosses", help="amount of bosses in each simulation (supports comma-separated lists)", default=1)
    parser.add_option("-c", "--cores", dest="cores", help="amount of threads to be used by SimulationCraft",default=4)
    parser.add_option("-o", "--output", dest="outputFile", help="output file name (base output file name for multiple simulations)", default=None)
    parser.add_option("-r", "--optimal-raid", action="store_true", dest="optimalRaid", help="toggles Optimal Raid setting", default=False)
    parser.add_option("-d", "--disable-bloodlust", action="store_true", dest="disableBloodlust", help="", default=False)
    parser.add_option("-l", "--log", dest="logFile", help="log file name (base log file name for multiple simulations)", default=None)
    parser.add_option("-y", "--plot-stats", dest="plotStats", help="the DPS stats that should be plotted (supports comma-separated lists)", default=None)
    parser.add_option("-z", "--plot-points", dest="plotPoints", help="the number of points to use to create the plot graph.", default=20)
    parser.add_option("-e", "--plot-steps", dest="plotStep", help=" is the delta between two points of the plot graph.", default=160.0)
    parser.add_option("-a", "--plot-target-error", dest="plotTargetError", help=" hopefully this works!", default=0.1)
    parser.add_option("-x", "--xml", dest="xmlFile", help="the xml output file name (base xml output file name for multiple simulations)", default='')
    parser.add_option("-j", "--json", dest="jsonFile", help="the json output file name (base json output file name for multiple simulations)", default='')
    parser.add_option("-2", "--json2", action="store_true", dest="json2", help="uses the experimental JSON2 output", default=False)
    parser.add_option("-k", "--resume-mode", action="store_true", dest="resumeMode", help="enables the resume mode. With this mode, simca won't do sims that have already been done (output file already exists)", default=False)
    parser.add_option("-n", "--scale-only", dest="scaleOnly", help="sets which stats to scale. Requires --scale-factors to work. Supports comma-separated lists.", default=None)

    (options, args) = parser.parse_args()

    global resumeMode
    global disableBloodlust
    global optimalRaid
    global scaleFactors
    global json2
    global scaleOnly

    if not options.profilename:
        print('Invalid profile name, please provide a valid one')
        return

    times = str(options.time) if not isinstance(options.time,str) else options.time
    resumeMode = options.resumeMode
    disableBloodlust = options.disableBloodlust
    optimalRaid = options.optimalRaid
    scaleFactors = 1 if options.scaleFactors else 0
    json2 = options.json2

    scaleOnly = options.scaleOnly.lower() if options.scaleOnly else None

    for time in times.split(","):
        for profile in options.profilename.split(","):
            for fight in options.fights.split(","):
                if isinstance(options.bosses,str):
                    for bossCount in options.bosses.split(","):
                        sim(profile, fight_reader(fight), options.iterations, time, options.variance, bossCount, options.cores, path.splitext(options.outputFile)[0] if options.outputFile else None, options.logFile, options.plotStats, options.plotPoints, options.plotStep, options.plotTargetError, path.splitext(options.xmlFile)[0], options.jsonFile)
                else:
                    sim(profile, fight_reader(fight), options.iterations, time, options.variance, options.bosses, options.cores, options.outputFile, options.logFile, options.plotStats, options.plotPoints, options.plotStep, options.plotTargetError, path.splitext(options.xmlFile)[0], options.jsonFile)

if __name__ == "__main__":
    main()
