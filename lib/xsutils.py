# Signal cross sections

import os

_xs_db = dict()
_xs_unc_db = dict()

# Disgusting fix for Higgs samples not correctly uploaded to PMG file:
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG?redirectedfrom=LHCPhysics.LHCHXSWG#Higgs_cross_sections_and_decay_b
HiggsSamplesXsecBR = {
    346198: 0.00155, # PhPy8EG_A14NNPDF23_NNPDF30ME_ttH125_Zgam
    346525: 0.00227, # PowhegPythia8EvtGen_A14NNPDF23_NNPDF30ME_ttH125_gamgam
}

def _create_xs_db():

    with open('/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc16.txt') as f:
        for line in f:
            line = line.replace('\n', '')
            if not line or line.startswith('#'):
                continue

            try:
                dsid, name, gen_xs, filter_eff, kfact, unc_up, unc_dn, gen_name, etag = line.split()
            except:
                continue

            # effective cross-section and relative uncertainty
            DSID = int(dsid)
            XSeff = float(gen_xs) * float(kfact) * float(filter_eff)
            XSUnc = max([float(unc_up), float(unc_dn)])

            if DSID in HiggsSamplesXsecBR:
                XSeff *= HiggsSamplesXsecBR[DSID]
                XSUnc *= HiggsSamplesXsecBR[DSID]

            _xs_db[DSID] = XSeff
            _xs_unc_db[DSID] = XSUnc


def get_xs_from_did(did):

    if not _xs_db:
        _create_xs_db()

    if did in _xs_db:
        return _xs_db[did]

    raise Exception('ERROR: XS not found for DID=%s' % (did))

