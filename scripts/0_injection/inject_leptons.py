import click

from icecube import dataio, icetray
from icecube.icetray import I3Tray

from upgrade_simulation_check.add_lepton import add_lepton

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

@click.command()
@click.option('--pdg_encoding', prompt="PDG encoding", help='PDG MC code for the lepton to be added', type=int)
@click.option('--elep', prompt="Lepton energy", help='Energy of the lepton (GeV)', type=float)
@click.option('--position', prompt="Optical module position", nargs=3, help='x,y,z, coordinates of the particle (m)', type=dumb_float)
@click.option('--outfile', prompt="Output file path", default="test_injection.i3.zst", help='Where to put the resulting I3 file')
@click.option('-n', prompt="Number of leptons to inject", default=100, help='How many leptons to inject', type=int)
def main(pdg_encoding, elep, position, outfile, n):
    tray = I3Tray()
    tray.AddModule(
        "I3InfiniteSource", "TheSource",
        Stream=icetray.I3Frame.DAQ
    )
    tray.AddModule(
        add_lepton,
        pdg_encoding=pdg_encoding,
        elep=elep,
        position=position,
        Streams=[icetray.I3Frame.DAQ]
    )
    tray.AddModule("I3Writer", 'writer', Filename=outfile)
    tray.AddModule("TrashCan", "trash")
    tray.Execute(n)

if __name__=="__main__":
    main()