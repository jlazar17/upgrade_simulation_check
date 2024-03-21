import numpy as np

from icecube.dataclasses import I3MCTree, I3Particle, I3Position, I3Direction
from icecube.icetray import I3Units, I3Frame

from typing import Tuple, Optional

def add_lepton(
    frame: I3Frame,
    pdg_encoding: int,
    elep: float, 
    position: Tuple[float] = (0.0, 0.0, 0.0),
    direction: Optional[Tuple[float]] = None
) -> None:
    lep = make_lepton(pdg_encoding, elep, position=position, direction=direction)
    mctree = I3MCTree()
    mctree.insert_after(lep)
    frame["I3MCTree"] = mctree
    return

def make_lepton(
    pdg_encoding: int,
    elep: float, 
    position: Tuple[float] = (0.0, 0.0, 0.0),
    direction: Optional[Tuple[float]] = None
) -> I3Particle:
    lep = I3Particle()
    lep.type = I3Particle.ParticleType(pdg_encoding)
    lep.energy = elep * I3Units.GeV
    lep.shape = I3Particle.Primary
    lep.location_type = I3Particle.InIce
    lep.time = 0.0 * I3Units.ns
    lep.pos= I3Position(
        position[0] * I3Units.m,
        position[1] * I3Units.m,
        position[2] * I3Units.m
    )
    if direction is None:
        rho = np.sqrt(position[0]**2 + position[1]**2)
        # Shoot it radially inward
        direction = (position[0] / rho, position[1] / rho, 0.0)
    
    lep.dir= I3Direction(
        direction[0],
        direction[1],
        direction[2]
    )
    return lep
