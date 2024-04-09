#! /bin/bash

INFILES=$@

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPTDIR/../setup.sh

for F in $INFILES
do
    F=`realpath $F`
    echo $F
    L=${#F}
    DESC=${F:$(($L-18)):11}
    
    echo $DESC
    $UPGRADEBUILDDIR/env-shell.sh \
        python clsim_mcpe_converter.py \
        --infile $F \
        --outfile $DATADIR/clsim_mcpe_no_geant/${DATAPREFIX}clsim_mcpe_no_geant_${DESC}.i3.zst \
        -g $GCDFILE\
        -a ANGSENS/angsens/${ANGSENS} \
        -e $NOMINALEFFICIENCY
done
