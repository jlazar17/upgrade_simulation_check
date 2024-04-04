#! /bin/bash

INFILES=$@

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPTDIR/../setup.sh

for F in $INFILES
do 
    F=`realpath $F`
    #echo $F
    L=${#F}
    DESC=${F:$(($L-18)):11}
    #echo $DESC
    ${GEN2BUILDDIR}/env-shell.sh \
        python $GEN2SRCDIR/simprod-scripts/resources/scripts/ppc.py \
        --inputfilelist $F \
        --outputfile $DATADIR/ppc_photons/${DATAPREFIX}ppc_photons_${DESC}.i3.zst \
        --gcdfile $GCDFILE \
        --oversize=$OVERSIZE \
        --UseGSLRNG \
        --StorePhotons --StorePhotonsSeries \
        --holeiceparametrization $ANGSENS \
        --IceModel $ICEMODEL \
        --KeepEmptyEvents \
        --no-UseGPUs
done
