"""Liste des venues non-Raydium v4 : propriétaires de réserves d'un programme AMM connu.

Une adresse découverte par dis_05 n'est un venue que si un programme AMM est présent dans au moins 80 %
de ses transactions à deux côtés. Sinon c'est un bot, un escrow DCA ou un autre wallet tenu par un
programme : il reste traité comme un trader.
"""
import json

from .config import ROOT

AMM = {
    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "raydium_clmm",
    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C": "raydium_cpmm",
    "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "meteora_dlmm",
    "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB": "meteora_amm",
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "orca_whirlpool",
    "PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY": "phoenix",
    "FLUXubRmkEi2q6K3Y9kBPg9248ggaZVsoSFhtJHSrm1X": "fluxbeam",
    "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA": "pumpswap",
}


def load() -> dict[str, str]:
    """adresse -> nom de venue."""
    data = json.loads((ROOT / "reports" / "data_checks" / "venues.json").read_text())
    out = {}
    for addr, v in data.items():
        if addr == "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1":
            continue
        for prog, name in AMM.items():
            if v["programs"].get(prog, 0) >= 0.8 * v["n_two_sided"]:
                out[addr] = name
                break
    return out
