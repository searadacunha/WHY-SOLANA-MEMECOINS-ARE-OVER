"""Synthetic, offline checks; never writes the published historical null."""
from pathlib import Path
import importlib.util
import json

MOD = Path(__file__).with_name("null_cohort_contamination.py")
spec = importlib.util.spec_from_file_location("null_cohort_contamination", MOD)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_same_launch_links_are_not_independent():
    pool = [
        {"wallet": "a", "token": "A", "funders": {"x"}},
        {"wallet": "b", "token": "A", "funders": {"x"}},
        {"wallet": "c", "token": "B", "funders": {"y"}},
        {"wallet": "d", "token": "B", "funders": {"z"}},
    ]
    res = mod.audit(pool, draws=20, group_sizes=(4,))
    assert res["shared_funder_pairs_within_launch"] == 1
    assert res["shared_funder_pairs_across_launches"] == 0
    assert res["sampled_rates_not_true_fpr"]["4"]["within"] == 1
    assert res["sampled_rates_not_true_fpr"]["4"]["across"] == 0
    assert res["can_construct_40_independent_launch_wallets"] is False


def test_cross_launch_and_within_can_coexist():
    pool = [
        {"wallet": "a", "token": "A", "funders": {"x"}},
        {"wallet": "b", "token": "A", "funders": {"x"}},
        {"wallet": "c", "token": "B", "funders": {"x"}},
    ]
    assert mod.funder_flags(pool) == (True, True)
    r = mod.audit(pool, draws=10, group_sizes=(3,))
    assert r["shared_funder_pairs_within_launch"] == 1
    assert r["shared_funder_pairs_across_launches"] == 2
    assert r["sampled_rates_not_true_fpr"]["3"]["both"] == 1


def test_loader_excludes_proceeds_and_terminal_addresses(tmp_path):
    raw = {"label": "A", "wallets": [
        {"wallet": "a", "inflows": [
            {"amount_sol": 1, "source": "private", "nature": "financement"},
            {"amount_sol": 2, "source": "ignore", "nature": "produit_de_vente"},
            {"amount_sol": 1, "source": next(iter(mod.KNOWN)), "nature": "financement"},
        ]},
    ]}
    (tmp_path / "e2_funding_A.json").write_text(json.dumps(raw))
    assert mod.load_pool(tmp_path)[0]["funders"] == {"private"}


def test_reused_wallet_across_launches_is_not_a_second_actor():
    """One address may participate in multiple launches without becoming two wallets."""
    pool = [
        {"wallet": "same", "token": "A", "funders": {"shared"}},
        {"wallet": "same", "token": "B", "funders": {"shared"}},
    ]
    assert mod.funder_flags(pool) == (False, False)
    r = mod.audit(pool, draws=10, group_sizes=(2,))
    assert r["wallet_observation_count"] == 2
    assert r["unique_wallet_addresses"] == 1
    assert r["reused_wallet_observations"] == 1
    assert r["shared_funder_pairs_within_launch"] == 0
    assert r["shared_funder_pairs_across_launches"] == 0
    assert r["sampled_rates_not_true_fpr"]["2"]["any"] == 0
