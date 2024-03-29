SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export DATADIR=`realpath $SCRIPTDIR/../data/`
export DATAPREFIX="upgrade_checks_"

export PYTHONPATH=$PYTHONPATH:$PWD/..

export GCDFILE="/data/sim/IceCubeUpgrade/geometries/GCDs/GeoCalibDetectorStatus_ICUpgrade.v58.mixed.V1.i3.bz2"
export GCDFILESTEP2="/data/sim/IceCubeUpgrade/geometries/GCDs/GeoCalibDetectorStatus_ICUpgrade.v58.sDOM.V1.i3.bz2"

export ANGSENS="as.flasher_p1_0.30_p2_-1"
export ICEMODEL="spice_bfr-v2"
export OVERSIZE=3
export GLASS=vitrovex
export EFFICIENCY=1.2

export DEGGREFX="14.29" # x-position of one of the DEggs that I found in `$GCDFILE`
export DEGGREFY="-80.5637" # y-position of one of the DEggs that I found in `$GCDFILE`
export DEGGREFZ="-601.93" # z-position of one of the DEggs that I found in `$GCDFILE`
