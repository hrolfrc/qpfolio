# tests/unit/test_plumbing_solver_info_schema.py
import types
from qpfolio.solvers.mathopt_osqp import _osqp_info_to_dict

def test_solver_info_schema_tolerance():
    # Simulate two OSQP versions:
    # vA: has pri_res/dua_res
    info_vA = types.SimpleNamespace(
        status="solved",
        obj_val=0.0,
        iter=42,
        status_val=1,
        pri_res=1e-6,
        dua_res=2e-6,
        setup_time=0.001,
        solve_time=0.002,
    )
    dA = _osqp_info_to_dict(info_vA)
    assert "pri_res" in dA and "dua_res" in dA
    assert dA["pri_res"] == 1e-6 and dA["dua_res"] == 2e-6

    # vB: only pri_res_norm/dua_res_norm
    info_vB = types.SimpleNamespace(
        status="solved",
        obj_val=0.0,
        iter=10,
        status_val=1,
        pri_res_norm=3e-6,
        dua_res_norm=4e-6,
    )
    dB = _osqp_info_to_dict(info_vB)
    assert "pri_res" in dB and "dua_res" in dB
    assert dB["pri_res"] == 3e-6 and dB["dua_res"] == 4e-6

    # vC: minimal info
    info_vC = types.SimpleNamespace(status="solved")
    dC = _osqp_info_to_dict(info_vC)
    # Fields exist but may be None
    assert "pri_res" in dC and "dua_res" in dC
