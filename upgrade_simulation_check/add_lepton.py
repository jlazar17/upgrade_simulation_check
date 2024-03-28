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
    nu = make_parent_nu(lep)
    mctree = I3MCTree()
    mctree.insert_after(nu)
    mctree.append_child(nu, lep)
    frame["I3MCTree"] = mctree
    return

def make_parent_nu(lep: I3Particle):
    nu = I3Particle()
    lep_pdg = int(lep.type)
    nu.type = I3Particle.ParticleType(int(np.sign(lep_pdg) + lep_pdg))
    nu.energy = 1.1 * lep.energy * I3Units.GeV
    nu.shape = I3Particle.Primary
    nu.location_type = I3Particle.InIce
    nu.time = 0.0 * I3Units.ns
    nu.pos = lep.pos
    nu.dir = lep.dir
    return nu

def make_lepton(
    pdg_encoding: int,
    elep: float, 
    position: Tuple[float] = (0.0, 0.0, 0.0),
    direction: Optional[Tuple[float]] = None
) -> I3Particle:
    lep = I3Particle()
    lep.type = I3Particle.ParticleType(pdg_encoding)
    lep.energy = elep * I3Units.GeV
    if int(lep.type) in [-15, 15, -13, 13]:
        lep.shape = I3Particle.StartingTrack
    else:
        lep.shape = I3Particle.Cascade
    lep.location_type = I3Particle.InIce
    lep.time = 0.0 * I3Units.ns
    lep.pos= I3Position(
        position[0] * I3Units.m,
        position[1] * I3Units.m,
        position[2] * I3Units.m
    )
    if direction is None:
        # pick a random direction chosen uniformly in phasespace
        theta = np.arccos(np.random.uniform(-1, 1))
        phi = np.random.uniform(0, 2*np.pi)
        xhat = np.cos(phi) * np.sin(theta)
        yhat = np.sin(phi) * np.sin(theta)
        zhat = np.cos(theta)
        direction = (xhat, yhat, zhat)
    
    lep.dir= I3Direction(
        direction[0],
        direction[1],
        direction[2]
    )
    return lep
