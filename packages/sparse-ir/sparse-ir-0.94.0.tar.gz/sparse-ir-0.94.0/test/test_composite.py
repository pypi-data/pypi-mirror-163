# Copyright (C) 2020-2022 Markus Wallerberger, Hiroshi Shinaoka, and others
# SPDX-License-Identifier: MIT
import numpy as np
import sparse_ir
from sparse_ir import poly
from sparse_ir import composite
from sparse_ir import augment

import pytest


def _check_composite_poly(u_comp, u_list, test_points):
    assert u_comp.size == np.sum([u.size for u in u_list])
    assert u_comp.shape == (u_comp.size,)
    np.testing.assert_allclose(u_comp(test_points),
                               np.vstack([u(test_points) for u in u_list]))
    idx = 0
    for isub in range(len(u_list)):
        for ip in range(u_list[isub].size):
            np.testing.assert_allclose(u_comp[idx](test_points),
                                       u_list[isub][ip](test_points))
            idx += 1


def test_composite_poly(sve_logistic):
    u, s, v = sve_logistic[42]
    l = s.size

    u_comp = composite.CompositeBasisFunction([u, u])
    _check_composite_poly(u_comp, [u, u], np.linspace(-1, 1, 10))

    uhat = poly.PiecewiseLegendreFT(u, "odd")
    uhat_comp = composite.CompositeBasisFunctionFT([uhat, uhat])
    _check_composite_poly(uhat_comp, [uhat, uhat], np.array([-3, 1, 5]))


def test_composite_basis(sve_logistic):
    beta = 7
    wmax = 6
    basis = sparse_ir.FiniteTempBasis("F", beta, wmax, eps=1e-6,
                                      sve_result=sve_logistic[beta * wmax])
    basis2 = sparse_ir.FiniteTempBasis("F", beta, wmax, eps=1e-3,
                                       sve_result=sve_logistic[beta * wmax])
    basis_comp = composite.CompositeBasis([basis, basis2])
    _check_composite_poly(basis_comp.u, [basis.u, basis2.u],
                          np.linspace(0, beta, 10))
    _check_composite_poly(basis_comp.uhat, [basis.uhat, basis2.uhat],
                          np.array([1,3]))
    assert basis_comp.beta == beta
    assert basis_comp.statistics == basis.statistics


def test_augmented_bosonic_basis():
    """Augmented bosonic basis"""
    wmax = 2
    beta = 1000
    basis = sparse_ir.FiniteTempBasis("B", beta, wmax, eps=1e-6)
    basis_legg = augment.LegendreBasis("B", beta, 2)
    basis_comp = composite.CompositeBasis([basis_legg, basis])

    # G(tau) = c - e^{-tau*pole}/(1 - e^{-beta*pole})
    pole = 1.0
    const = 1e-2
    tau_smpl = sparse_ir.TauSampling(basis_comp)
    gtau = const + basis.u(tau_smpl.tau).T @ (-basis.s * basis.v(pole))
    magn = np.abs(gtau).max()

    # This illustrates that "naive" fitting is a problem if the fitting matrix
    # is not well-conditioned.
    gl_fit_bad = np.linalg.pinv(tau_smpl.matrix) @ gtau
    gtau_reconst_bad = tau_smpl.evaluate(gl_fit_bad)
    assert not np.allclose(gtau_reconst_bad, gtau, atol=1e-13 * magn, rtol=0)
    np.testing.assert_allclose(gtau_reconst_bad, gtau,
                               atol=5e-16 * tau_smpl.cond * magn, rtol=0)

    # Now do the fit properly
    gl_fit = tau_smpl.fit(gtau)
    gtau_reconst = tau_smpl.evaluate(gl_fit)
    np.testing.assert_allclose(gtau_reconst, gtau, atol=1e-14 * magn, rtol=0)


@pytest.mark.parametrize("stat", ["F", "B"])
def test_vertex_basis(stat):
    """Vertex basis"""
    wmax = 2
    beta = 1000
    basis = sparse_ir.FiniteTempBasis(stat, beta, wmax, eps=1e-6)
    basis_const = augment.MatsubaraConstBasis(stat, beta)
    basis_comp = composite.CompositeBasis([basis_const, basis])
    assert basis_comp.uhat is not None

    # G(iv) = c + 1/(iv-pole)
    pole = 1.0
    c = 1.0
    matsu_smpl = sparse_ir.MatsubaraSampling(basis_comp)
    giv = c  + 1/(1J*matsu_smpl.sampling_points * np.pi/beta - pole)
    gl = matsu_smpl.fit(giv)

    giv_reconst = matsu_smpl.evaluate(gl)

    np.testing.assert_allclose(giv, giv_reconst,
                               atol=np.abs(giv).max() * 1e-7, rtol=0)
