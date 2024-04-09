is_gen1 = lambda om: om.string<=86
is_upgrade = lambda om: om.string > 86
is_ref_degg = lambda om: om.string==93 and om.om==121
