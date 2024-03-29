#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/icetray-start
#METAPROJECT /data/user/mlarson/icetray/build/
##!/usr/bin/env python3

'''
Modified from `/data/user/mlarson/icetray/scripts/upgrade_sim/psu_to_mcpes/just_mcpe.py`

Modified Upgrade MC step3 to produce MCPEs that can be used in simprods detectorsim

This is configured with low energy (Upgrade/DeepCore) events in mind
'''


from optparse import OptionParser
import os, sys
from os.path import expandvars
from copy import deepcopy

from icecube import dataio, dataclasses, icetray, phys_services, simclasses
from icecube.icetray import I3Units
from I3Tray import *
import numpy as np

icetray.logging.set_level(icetray.logging.I3LogLevel.LOG_INFO)


#
# Get args
#

usage = "usage: %prog [options]"
parser = OptionParser(usage)
# File IO args...
parser.add_option("-o", "--outfile",
                  dest="OUTFILE", help="Write output to OUTFILE (.i3{.gz} format)")
parser.add_option("-i", "--infile",
                  dest="INFILE", help="Read input from INFILE (.i3{.gz} format)")
parser.add_option("-g", "--gcdfile", default=os.getenv('GCDfile'),
                  dest="GCDFILE", help="Read in GCD file")
# Noise related args...
parser.add_option("-b", "--mdomglass", default="vitrovex",
                  dest="GLASS", help="mDOM Glass")
# Ice and detector args...
#parser.add_option("-m","--icemodel", default="spice_lea",
#                   dest="ICEMODEL",help="Ice model (spice_mie, spice_lea, etc)")
parser.add_option("-a", "--holeice",  default=None, dest="HOLEICE",
                  help="Pick the hole ice parameterization, corresponds to a file name path relative to $I3_SRC/ice-models/resources/models/")
parser.add_option("-e","--efficiency", default=None, action='append',
                  dest="EFFICIENCY",help="Module Efficiencies")
# Other
parser.add_option("--nevents",type="int",default=None, # Only for noise-only events
                  dest="NEVENTS", help="Number of noise frames to create")
(options,args) = parser.parse_args()

if len(args) != 0:
    crap = "Got undefined options:"
    for a in args:
        crap += a
        crap += " "
        parser.error(crap)

assert options.INFILE is not None, "Must provide an input file"
assert options.NEVENTS is None, "Cannot specify number of events unless in noise-only mode"
#assert options.ICEMODEL is not None
assert options.HOLEICE is not None
assert options.EFFICIENCY is not None

# Reporting
print("Settings :")
print("  GCD file : %s" % options.GCDFILE)

#print("  Ice model : %s" % options.ICEMODEL)
print("  Hole ice model : %s" % options.HOLEICE)
print("  Efficiencies : %s" % options.EFFICIENCY)


#
# IceTray
#

def step_3_icetray(gcd_file, input_file, output_file) :
    '''
    The step3 icetray job
    Using a decorator to add gridftp file I/O support
    '''
    #
    # Start up
    #

    # Create tray
    tray = I3Tray()

    # RNG seeding
    seed = 0
    streamnum =0
    nstreams =  100000

    # Create RNG
    randomService = phys_services.I3SPRNGRandomService(
        seed=seed,
        nstreams=nstreams,
        streamnum=streamnum,
    )

    # Also RNG servce with same settings #TODO why?
    tray.AddService("I3SPRNGRandomServiceFactory", "sprngrandom")(
            ("Seed", seed),
            ("StreamNum", streamnum),
            ("NStreams", nstreams),
            ("instatefile",""),
            ("outstatefile",""),
    )

    # Create driver
    # Input file reader
    tray.AddModule('I3Reader', 'reader', FilenameList=[gcd_file, input_file])


    #
    # Get sensor definitions
    #

    ##########
    # Need to determine which to use from GCD file. For now, use everything
    # except WOMs, which we don't have properly implemented.
    ##########
    from icecube.gen2_sim.utils import ModuleToString, FindModuleTypes
    Sensors, EfficiencyScales, MCPEs = FindModuleTypes(gcd_file)

    if not options.EFFICIENCY is None:
        EfficiencyScales *= np.array(options.EFFICIENCY).astype(float)

    print("GCD file contains modules with these sensor types:")
    for i, Sensor in enumerate(Sensors):
        print('\t ', ModuleToString(Sensor, Prefix=''), '(EfficiencyScale:', EfficiencyScales[i], ')')

    ##########
    # Determine whether we have to redo the painfully slow BadDomList calculation
    # or if we already have an existing BDL that we can use.
    ##########
    from icecube.gen2_sim.utils import HasBadDomList
    RedoBadDomList = not HasBadDomList(gcd_file)
    print('Redo BadDomList:', RedoBadDomList)


    #
    # Process input photons
    #

    # Remove any late photons
    from icecube.gen2_sim.utils import RemoveLatePhotons
    tray.AddModule(
        RemoveLatePhotons,
        "RemovePhotons",
        InputPhotonSeries = "I3PhotonSeriesMap",
        TimeLimit = 1E5, # ns
    )

    # Convert MCPE to photons
    from icecube.gen2_sim.segments.clsim import MakePEFromPhotons
    tray.Add(
        MakePEFromPhotons,
        Sensors=Sensors,
        GCDFile=gcd_file,
        # MCTreeName="I3MCTree_sliced", # Removed during sync with gen2-optical-sim
        PhotonSeriesName="I3PhotonSeriesMap",
        DOMOversizeFactor=1., #TODO same as step2?
        EfficiencyScales=EfficiencyScales,
        RandomService=randomService,
        HoleIceParameterization = expandvars("$I3_SRC/ice-models/resources/models/" + options.HOLEICE),
        HoleIceParameterizationGen2 =  expandvars("$I3_SRC/ice-models/resources/models/" + options.HOLEICE), # Doesn't support hole ice currently
        UseDefaultRPEValue = True, # Use the default Relative PMT Efficiency (RPE) values for DEgg and mDOM
    )


    from icecube.simclasses import I3MCPESeriesMap
    def merge_mcpes(frame):
        old_names = ['I3MCPESeriesMap_DEgg',
                     'I3MCPESeriesMap_IceCube',
                     'I3MCPESeriesMap_PDOM',
                     'I3MCPESeriesMap_mDOM',]
        new_mcpes = I3MCPESeriesMap()
        
        for old_map_name in old_names:
            old_map = frame[old_map_name]
            for omk, mcpes in old_map.items():
                new_mcpes[omk] = mcpes
            del frame[old_map_name]
            
            
        # Clear these too while I'm here...
        del frame['I3PhotonSeriesMap']

        frame['I3MCPESeriesMap'] = new_mcpes
        return
    
    tray.Add(merge_mcpes,
             Streams = [icetray.I3Frame.DAQ,])                     

    # Write output files
    tray.AddModule(
        "I3Writer",
        "writer",
        Filename=output_file,
        Streams=[icetray.I3Frame.Simulation, icetray.I3Frame.TrayInfo, icetray.I3Frame.DAQ],
    )

    # Run
    tray.Execute()
    tray.Finish()

#
# Run
#

step_3_icetray(
    gcd_file=options.GCDFILE,
    output_file=options.OUTFILE,
    input_file=options.INFILE,
)
