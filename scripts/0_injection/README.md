# About

Checks we done using the `gen2_simprod` branch of icetray at commit `7c15abc2144e7dcd7e7829c0df1de1a6fc68d839`.
The injection is very simple and places a $e^{\pm}$ or $\mu^{\pm}$ with an input energy at a random position and random initial direction.
The sampling is done independently of icetray and so we should not expect differences between the OscNext and Gen2 branches.

# Usage

First we need to load our icetray environment.
Change this as appropriate

```bash
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh`
source /data/user/jlazar/icetrays/Gen2Sim/build/env-shell.sh
```

The we need to source the global variables from the `setup.sh`

```bash
source ../setup.sh
```

Now we inject at a offset from a reference DEgg position

```bash
E=5 # GeV
PDG=11 # Electron
OFFSET=4 # m

python inject_leptons.py \
    --position $DEGGREFX+$OFFSET $DEGGREFY $DEGGREFZ \
    --elep $E \
    --pdg_encoding $PDG \
    --outfile $DATADIR/${DATAPREFIX}injection.i3.zst \
    -n 1000
```

You can also use the `run_injection.sh`, which will inject at the same offset along the positive and negative $x$-, $y$-, and $z$-directions.

```bash
./run_injection 5 11 4
```
