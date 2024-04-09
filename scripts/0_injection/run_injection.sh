#! /bin/bash

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPTDIR/../setup.sh

E=$1
PDG=$2
OFFSET=$3

${GEN2BUILDDIR}/env-shell.sh python inject_leptons.py --position $DEGGREFX+$OFFSET $DEGGREFY $DEGGREFZ --elep $E --pdg_encoding $PDG --outfile $DATADIR/injection/${DATAPREFIX}injection_${PDG}_${E}_p${OFFSET}p0p0.i3.zst -n 1000
${GEN2BUILDDIR}/env-shell.sh python inject_leptons.py --position $DEGGREFX-$OFFSET $DEGGREFY $DEGGREFZ --elep $E --pdg_encoding $PDG --outfile $DATADIR/injection/${DATAPREFIX}injection_${PDG}_${E}_n${OFFSET}p0p0.i3.zst -n 1000
${GEN2BUILDDIR}/env-shell.sh python inject_leptons.py --position $DEGGREFX $DEGGREFY+$OFFSET $DEGGREFZ --elep $E --pdg_encoding $PDG --outfile $DATADIR/injection/${DATAPREFIX}injection_${PDG}_${E}_p0p${OFFSET}p0.i3.zst -n 1000
${GEN2BUILDDIR}/env-shell.sh python inject_leptons.py --position $DEGGREFX $DEGGREFY-$OFFSET $DEGGREFZ --elep $E --pdg_encoding $PDG --outfile $DATADIR/injection/${DATAPREFIX}injection_${PDG}_${E}_p0n${OFFSET}p0.i3.zst -n 1000
${GEN2BUILDDIR}/env-shell.sh python inject_leptons.py --position $DEGGREFX $DEGGREFY $DEGGREFZ+$OFFSET --elep $E --pdg_encoding $PDG --outfile $DATADIR/injection/${DATAPREFIX}injection_${PDG}_${E}_p0p0p${OFFSET}.i3.zst -n 1000
${GEN2BUILDDIR}/env-shell.sh python inject_leptons.py --position $DEGGREFX $DEGGREFY $DEGGREFZ-$OFFSET --elep $E --pdg_encoding $PDG --outfile $DATADIR/injection/${DATAPREFIX}injection_${PDG}_${E}_p0p0n${OFFSET}.i3.zst -n 1000
