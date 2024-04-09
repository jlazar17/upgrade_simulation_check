import numpy as np

from icecube import dataio
from icecube.icetray import I3Frame
from typing import Callable

NO_FILTER = lambda om: True
MCPEMAPNAME = "I3MCPESeriesMap"


def count_helper(
    frame: I3Frame,
    ct_fxn: Callable,
    filter: Callable=NO_FILTER,
    mcpemapname:str=MCPEMAPNAME
) -> int:
    map = frame[mcpemapname]
    n = 0
    for om, mcpelist in map.items():
        if not filter(om):
            continue
        n += ct_fxn(mcpelist)
    return n

def count_mcpe(
    frame: I3Frame,
    filter=NO_FILTER,
    mcpemapname:str=MCPEMAPNAME
) -> int:
    n = count_helper(
        frame,
        lambda mcpelist: len(mcpelist),
        filter=filter,
        mcpemapname=mcpemapname
    )
    return n

def count_module(
    frame: I3Frame,
    filter=NO_FILTER,
    mcpemapname:str=MCPEMAPNAME
) -> int:
    n = count_helper(
        frame,
        lambda _: 1,
        filter=filter,
        mcpemapname=mcpemapname
    )
    return n

def get_count_vars(
    f:str,
    filter: Callable=NO_FILTER,
    mcpemapname: str=MCPEMAPNAME,
    ninjected: int=1000
):
    i3f = dataio.I3File(f)
    x = []
    y = []
    while i3f.more():
        frame = i3f.pop_daq()
        x.append(count_mcpe(frame, filter=filter, mcpemapname=mcpemapname))
        y.append(count_module(frame, filter=filter, mcpemapname=mcpemapname))
    i3f.close()
    nmodules, nmcpes = np.zeros(ninjected), np.zeros(ninjected)
    nmcpes[:len(x)] = x
    nmodules[:len(y)] = y
    return nmcpes, nmodules

def count_hits_per_module(f: str, neventmin=1, mcpemapname=MCPEMAPNAME):
    i3f = dataio.I3File(f)
    d = {}
    while i3f.more():
        frame = i3f.pop_daq()
        for k, v in frame[mcpemapname].iteritems():
            if k not in d:
                d[k] = []
            d[k].append(len(v))
    d = {k:v for k, v in d.items() if len(v) >= neventmin}
    return d

def _mcpe_timing_frame(
    frame: I3Frame,
    filter: Callable=NO_FILTER,
    mcpemapname: str=MCPEMAPNAME
):
    times = np.array([])
    for om, v in frame[mcpemapname].iteritems():
        if not filter(om):
            continue
        times = np.append(times, [x.time for x in v])
    return times

def mcpe_timing(
    f: str,
    filter: Callable=NO_FILTER,
    mcpemapname=MCPEMAPNAME
):
    times = []
    i3f = dataio.I3File(f)
    while i3f.more():
        frame = i3f.pop_daq()
        times.append(_mcpe_timing_frame(frame, filter=filter, mcpemapname=mcpemapname))
    i3f.close()
    return times
