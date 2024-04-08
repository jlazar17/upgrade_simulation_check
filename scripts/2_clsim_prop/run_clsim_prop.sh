#! /bin/bash

INFILES=$@

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPTDIR/../setup.sh

RANDN=$RANDOM

for F in $INFILES
do
    F=`realpath $F`
    L=${#F}
    DESC=${F:$(($L-18)):11}
    
    $UPGRADEBUILDDIR/env-shell.sh \
        python ${UPGRADESRCDIR}/oscNext/resources/scripts/mc_production/step2_G4_photon_prop.py \
        --infile $F \
        --outfile $DATADIR/clsim_photons/${DATAPREFIX}clsim_photons_${DESC}.i3.zst \
        -g $GCDFILESTEP2 \
        -r $RANDN -l $RANDN \
        -a ANGSENS/angsens/${ANGSENS} \
        -m ICEMODEL/${ICEMODEL} \
        --oversize ${OVERSIZE} \
        -e $MAXEFFICIENCY
done
