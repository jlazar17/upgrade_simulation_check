# About

This step will propagate the photons produced by the injected charged leptons to the surface of the OMs using CLSim.
This relies on the `icecube_upgrade` branch of icetray.
At this time of the writing the version on GitHub did not compile directly, and so I used a precompiled version in the CVMFS.

# Usage

If you are in the environment from the previous two steps, you will need to `exit` the shell and then run

```bash
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
/cvmfs/icecube.opensciencegrid.org/users/upgrade-sim/software/icetray/branches/icecube_upgrade/build__py3-v4.2.1/env-shell.sh
```

The we need to source the global variables from the `setup.sh`

```bash
cd ..
source setup.sh
cd 2_clsim_prop
```

Note that the `-l` and `-r` flags are used for random number seeding and so they should be changed on a per-run basis

```bash
python ${I3_SRC}/oscNext/resources/scripts/mc_production/step2_G4_photon_prop.py \
    --infile $DATADIR/${DATAPREFIX}injection.i3.zst \
    --outfile $DATADIR/${DATAPREFIX}clsim_photons.i3.zst \
    -g $GCDFILESTEP2 \
    -r 925 -l 925 \
    -m ICEMODEL/${ICEMODEL} \
    -a ANGSENS/angsens/${ANGSENS} \
    --oversize ${OVERSIZE}
```