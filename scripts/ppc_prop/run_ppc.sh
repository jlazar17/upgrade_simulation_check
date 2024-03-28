#! /bin/bash

INFILES=$@
for INFILE in $INFILES; do

    L=${#INFILE}
    S=$((L-18))
    DESC=${INFILE:S:100}
    OUTFILE=$DATADIR/${DATAPREFIX}ppc_photons_${DESC}
    
    CMD="$I3_BUILD/env-shell.sh python $I3_SRC/simprod-scripts/resources/scripts/ppc.py --inputfilelist=${INFILE} --outputfile $OUTFILE --gcdfile=$GCDFILE --oversize=5 --UseGSLRNG --StorePhotonsSeries --no-UseGPUs --StorePhotons"
    $CMD
    echo $CMD
done
