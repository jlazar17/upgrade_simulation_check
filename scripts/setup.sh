export DATADIR=`realpath $PWD/../data/`
export DATAPREFIX="upgrade_checks_"

export PYTHONPATH=$PYTHONPATH:$PWD/..

export GCDFILE="/data/sim/IceCubeUpgrade/genie/step3/140029/GeoCalibDetectorStatus_ICUpgrade.v58.mixed.V1.i3.bz2"
export GCDFILESTEP2="/data/sim/IceCubeUpgrade/genie/step3/140029/GeoCalibDetectorStatus_ICUpgrade.v58.sDOM.V1.i3.bz2 "

export ANGSENS="as.flasher_p1_0.30_p2_-1"
export ICEMODEL="spice_bfr-v2"

export DEGGREFX="14.29" # x-position of one of the DEggs that I found in `$GCDFILE`
export DEGGREFY="-80.5637" # y-position of one of the DEggs that I found in `$GCDFILE`
export DEGGREFZ="-601.93" # z-position of one of the DEggs that I found in `$GCDFILE`
