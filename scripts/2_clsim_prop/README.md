# Usage

Note that the `-l` and `-r` flags are used for random number seeding and so they should be changed on a per-run basis

```bash
python ${I3_SRC}/oscNext/resources/scripts/mc_production/step2_G4_photon_prop.py \
    --infile $DATADIR/${DATAPREFIX}injection.i3.zst \
    --outfile $DATADIR/${DATAPREFIX}clsim_photons.i3.zst \
    -g $GCDFILESTEP2 \
    -r 925 -l 925 \
    -m ICEMODEL/${ICEMODEL} \
    -a ANGSENS/angsens/{ANGSENS}
```
