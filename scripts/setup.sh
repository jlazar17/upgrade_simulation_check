SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export DATADIR=`realpath $SCRIPTDIR/../data/`
export DATAPREFIX="upgrade_checks_"

export UPGRADEBUILDDIR=/data/user/jlazar/icetrays/Upgrade/build/
export UPGRADESRCDIR=/data/user/jlazar/icetrays/Upgrade/src/
export GEN2BUILDDIR=/data/user/jlazar/icetrays/Gen2Sim/build/
export GEN2SRCDIR=/data/user/jlazar/icetrays/Gen2Sim/src/

export PYTHONPATH=$PYTHONPATH:$SCRIPTDIR/..

export GCDFILE="/data/sim/IceCubeUpgrade/geometries/GCDs/GeoCalibDetectorStatus_ICUpgrade.v58.mixed.V1.i3.bz2"
export GCDFILESTEP2="/data/sim/IceCubeUpgrade/geometries/GCDs/GeoCalibDetectorStatus_ICUpgrade.v58.sDOM.V1.i3.bz2"

export ANGSENS="as.nominal"
export ICEMODEL="spice_bfr-v2"
export OVERSIZE=1 # CLSim will blow a gasket when converting to MCPE if this isn't 1
export GLASS=vitrovex
export MAXEFFICIENCY=1.2
export NOMINALEFFICIENCY=1.0

export DEGGREFX="14.29" # x-position of one of the DEggs that I found in `$GCDFILE`
export DEGGREFY="-80.5637" # y-position of one of the DEggs that I found in `$GCDFILE`
export DEGGREFZ="-601.93" # z-position of one of the DEggs that I found in `$GCDFILE`
