# Example usage

First you have to edit the setup script to change paths and such if you want.
Then you can 
```bash
source setup.sh
```

To produce the initial injection run
```bash
python inject_leptons.py --position 50 50 -500 --elep 4.5 --pdg_encoding 13 --outfile $DATADIR/${DATAPREFIX}injection.i3.zst -n 1000
```

Then to run this through `PPC`, run

```bash
python $I3_SRC/simprod-scripts/resources/scripts/ppc.py --inputfilelist=$DATADIR/${DATAPREFIX}injection.i3.zst --outputfile $DATADIR/${DATAPREFIX}ppc_photons.i3.zst --gcdfile=$GCDFILE --oversize=5 --UseGSLRNG --StorePhotons
```

If you are not on a device with a GPU, you can instead run

```bash
python $I3_SRC/simprod-scripts/resources/scripts/ppc.py --inputfilelist=$DATADIR/${DATAPREFIX}injection.i3.zst --outputfile $DATADIR/${DATAPREFIX}ppc_photons.i3.zst --gcdfile=$GCDFILE --oversize=5 --UseGSLRNG --StorePhotons --no-UseGPUs
```

Then we need to run the injection through `CLSim`

```bash
```
