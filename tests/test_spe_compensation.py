import os
import numpy as np

import icecube
from icecube import dataio, dataclasses, simclasses

NPMTS_PER_MODULE = {
    "PDOM": 1.0,
    "IceAct": 1.0,
    "IceCube": 1.0,
    "IceTop": 1.0,
    "Scintillator": 1.0,
    "DEgg": 2.0,
    "mDOM": 24.0
}

def test_all_pmts_have_compensation():
    gcd = dataio.I3File(os.environ["GCDFILE"])
    # Gotta pop twice to get the calibration frame
    _ = gcd.pop_frame()
    cal_frame = gcd.pop_frame()
    geomap = cal_frame["I3ModuleGeoMap"]
    dc = cal_frame["I3Calibration"].dom_cal
    module_counter = {}
    pmt_spe_compensation_counter = {}
    seen_oms = []
    for pmtkey, v in dc.iteritems():
        omkey = dataclasses.ModuleKey(pmtkey.string, pmtkey.om)
        omgeo = geomap[omkey]
        if str(omgeo.module_type) not in module_counter:
            module_counter[str(omgeo.module_type)] = 0
        if str(omgeo.module_type) not in pmt_spe_compensation_counter:
            pmt_spe_compensation_counter[str(omgeo.module_type)] = []
        if omkey not in seen_oms:
            module_counter[str(omgeo.module_type)] += 1
            seen_oms.append(omkey)
        pmt_spe_compensation_counter[str(omgeo.module_type)].append(v.combined_spe_charge_distribution.compensation_factor)
    for k in module_counter.keys():
        assert NPMTS_PER_MODULE[k] == len(pmt_spe_compensation_counter[k]) / module_counter[k]

def test_spe_compensation_consistent():
    gcd1 = dataio.I3File(os.environ["GCDFILE"])
    _ = gcd1.pop_frame()
    cal1 = gcd1.pop_frame()
    gcd2 = dataio.I3File(os.environ["GCDFILESTEP2"])
    _ = gcd2.pop_frame()
    cal2 = gcd2.pop_frame()
    dc1 = cal1["I3Calibration"].dom_cal
    dc2 = cal2["I3Calibration"].dom_cal
    for k in dc1.iterkeys():
        f1 = dc1[k].combined_spe_charge_distribution.compensation_factor
        f2 = dc2[k].combined_spe_charge_distribution.compensation_factor
        assert f1==f2, f"{f1}, {f2} k"
    for k in dc2.iterkeys():
        f1 = dc1[k].combined_spe_charge_distribution.compensation_factor
        f2 = dc2[k].combined_spe_charge_distribution.compensation_factor
        assert f1==f2
