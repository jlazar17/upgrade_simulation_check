import click

from icecube import dataio, icetray
from icecube.icetray import I3Tray

from upgrade_simulation_check.add_lepton import add_lepton

def initialize_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        "--pdg_encoding",
        type=int,
        required=True,
        help="PDG code of the charged lepton to inject"
    )
    parser.add_argument(
        "--elep",
        type=float,
        required=True,
        help="Energy of the lepton in GeV"
    )
    parser.add_argument(
        "--position",
        type=float,
        nargs=3,
        required=True,
        help="x y z position at which to inject the particle"
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        required=True,
        help="Output i3 file name"
    )
    parser.add_argument(
        "-n",
        type=int,
        help="How many leptons to inject at input position"m
        default=100
    )
    return parser.parse_args()

def dumb_float(x):
    splitchar = "+" if "+" in x else "-"
    op = "__add__" if "+" in x  else "__sub__"
    splitx = x.split(splitchar)
    if x[0]=="-":
        splitx = splitx[1:]
    y = float(splitx[0])
    if x[0]=="-":
        y *= -1
    for yp in splitx[1:]:
        y = getattr(y, op)(float(yp))
    return y

def main():
    args = initialize_args()
    tray = I3Tray()
    tray.AddModule(
        "I3InfiniteSource", "TheSource",
        Stream=icetray.I3Frame.DAQ
    )
    tray.AddModule(
        add_lepton,
        pdg_encoding=args.pdg_encoding,
        elep=args.elep,
        position=args.position,
        Streams=[icetray.I3Frame.DAQ]
    )
    tray.AddModule("I3Writer", 'writer', Filename=args.outfile)
    tray.AddModule("TrashCan", "trash")
    tray.Execute(args.n)

if __name__=="__main__":
    main()
