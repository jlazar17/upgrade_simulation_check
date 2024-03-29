# About

Checks we done using the `gen2_simprod` branch of icetray at commit `7c15abc2144e7dcd7e7829c0df1de1a6fc68d839`

# Usage

First we need to load our icetray environment.
Change this as appropriate

```bash
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
source /data/user/jlazar/icetrays/Gen2Sim/build/env-shell.sh
```

The we need to source the global variables from the `setup.sh`

```bash
cd ..
source setup.sh
cd 1_ppc_prop
```

```bash
python $I3_SRC/simprod-scripts/resources/scripts/ppc.py \
    --inputfilelist $DATADIR/${DATAPREFIX}injection.i3.zst \
    --outputfile $DATADIR/${DATAPREFIX}ppc_photons.i3.zst \
    --gcdfile $GCDFILE \
    --oversize=$OVERSIZE \
    --UseGSLRNG \
    --StorePhotons --StorePhotonsSeries \
    --holeiceparametrization $ANGSENS \
    --IceModel $ICEMODEL
```

If you are not on a device with a GPU, you can instead run

```bash
python $I3_SRC/simprod-scripts/resources/scripts/ppc.py \
    --inputfilelist $DATADIR/${DATAPREFIX}injection.i3.zst \
    --outputfile $DATADIR/${DATAPREFIX}ppc_photons.i3.zst \
    --gcdfile $GCDFILE \
    --oversize=$OVERSIZE \
    --UseGSLRNG \
    --StorePhotons --StorePhotonsSeries \
    --holeiceparametrization $ANGSENS \
    --IceModel $ICEMODEL \
    --no-UseGPUs
```


