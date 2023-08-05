import pytest
from weaveio import *


def test_rerun(data):
    l2s = data.l2stacks
    l2s = l2s[any(l2s.fibre_target.surveys == '/WL.*/', wrt=l2s)]
    l2s = l2s[l2s['ha_6562.80_flux'] > 0]
    ratio = l2s['[oiii]_5006.77_flux'] / l2s['ha_6562.80_flux']
    max(ratio)
    ratio = l2s['[oiii]_5006.77_flux'] / l2s['ha_6562.80_flux']
    one_l2 = l2s[max(ratio) == ratio]
    t = one_l2[['[oiii]_5006.77_flux', 'ha_6562.80_flux', 'cname']]
    cname1 = t()['cname'][0]
    l2s = l2s[l2s['[oiii]_5006.77_flux'] > 0]
    ratio = l2s['[oiii]_5006.77_flux'] / l2s['ha_6562.80_flux']
    one_l2 = l2s[max(ratio) == ratio]
    t = one_l2[['[oiii]_5006.77_flux', 'ha_6562.80_flux', 'cname']]
    cname2 = t()['cname'][0]
    assert cname2 == cname1


def test_rerun_with_limit(data):
    obs = data.obs.id
    assert np.all(obs(limit=10) == obs(limit=10))


def test_merge_tables(data):
    def noise_spectra_query(parent, camera, targuse='S', split_into_subqueries=True):
        if split_into_subqueries:
            parent = split(parent)
        stacks = parent.l1stack_spectra[(parent.l1stack_spectra.targuse == targuse) & (parent.l1stack_spectra.camera == camera)]
        singles = stacks.l1single_spectra
        singles_table = singles[['flux', 'ivar']]
        query = stacks[['ob.id', {'stack_flux': 'flux', 'stack_ivar': 'ivar'}, 'wvl', {'single_': singles_table}]]
        return query

    for index, query in noise_spectra_query(data.obs, 'red'):
        t = query(limit=1)
        assert t['ob.id'] == index
        assert len(t['stack_flux'].shape) == 1
        assert len(t['single_flux'].shape) == 2
        break