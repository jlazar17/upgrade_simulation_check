# About

Checks we done using the `gen2_simprod` branch of icetray at commit `7c15abc2144e7dcd7e7829c0df1de1a6fc68d839`

# Usage

```bash
python $I3_SRC/simprod-scripts/resources/scripts/ppc.py \
    --inputfilelist $DATADIR/${DATAPREFIX}injection.i3.zst \
    --outputfile $DATADIR/${DATAPREFIX}ppc_photons.i3.zst \
    --gcdfile $GCDFILE \
    --oversize=5 \
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
    --oversize=5 \
    --UseGSLRNG \
    --StorePhotons --StorePhotonsSeries \
    --holeiceparametrization $ANGSENS \
    --IceModel $ICEMODEL \
    --no-UseGPUs
```
