#! /bin/bash

PDG=$1

OUTFILE=$DATADIR/${DATAPREFIX}ppc_photons_${PDG}.i3.zst
TMPFILE=tmp_${PDG}.txt
for F in `ls $DATADIR/upgrade_checks_injection_${PDG}_*`; do 
    REALF=`realpath ${F}`
    echo -n $REALF, >> ${TMPFILE}
done
echo `cat $TMPFILE | sed -r '$s/.{1}$//'` > $TMPFILE

python $I3_SRC/simprod-scripts/resources/scripts/ppc.py \
    --inputfilelist `cat $TMPFILE` \
    --outputfile $OUTFILE \
    --gcdfile $GCDFILE \
    --oversize=5 \
    --UseGSLRNG \
    --StorePhotons --StorePhotonsSeries \
    --holeiceparametrization $ANGSENS \
    --IceModel $ICEMODEL \
    --no-UseGPUs

rm $TMPFILE
