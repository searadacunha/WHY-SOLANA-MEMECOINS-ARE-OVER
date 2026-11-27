"""Comptabilité par wallet au coût moyen pondéré. Le réalisé ne compte que le SOL réellement reçu.

Conventions :
- Achat : quantité + et coût + (SOL entré dans le pool ou la courbe, frais de plateforme non inclus).
- Vente : réalisé = produit - coût moyen de la quantité vendue. La part vendue au-delà de la quantité
  connue (jetons d'origine inconnue) entre dans `sold_no_basis_qty`, sans coût, et reste signalée.
- Transfert entrant : quantité + sans coût, signalé. Transfert sortant : retire la quantité et son coût
  moyen, signalé. Le réalisé d'un wallet qui reçoit ses jetons d'un autre wallet est donc surévalué,
  d'où le champ `completeness`.
"""
from dataclasses import dataclass, field


@dataclass
class Wallet:
    owner: str
    qty: int = 0
    cost: float = 0.0  # lamports
    realized: float = 0.0  # lamports
    bought_qty: int = 0
    bought_sol: int = 0
    sold_qty: int = 0
    sold_sol: int = 0
    n_buys: int = 0
    n_sells: int = 0
    transfer_in_qty: int = 0
    transfer_out_qty: int = 0
    n_transfers: int = 0
    sold_no_basis_qty: int = 0
    lp_token_in: int = 0  # jetons déposés en liquidité par le wallet
    lp_token_out: int = 0  # jetons récupérés de ses positions
    lp_sol_in: int = 0
    lp_sol_out: int = 0
    first_buy_time: int | None = None
    first_buy_sig: str | None = None
    first_buy_slot: int | None = None
    first_buy_tx_index: int | None = None
    first_buy_sol: int | None = None
    first_buy_qty: int | None = None
    first_sell_time: int | None = None
    last_sell_time: int | None = None
    last_activity_time: int | None = None
    min_qty: int = 0
    venues: set = field(default_factory=set)

    def apply(self, kind: str, token_delta: int, sol_lamports: int, t: int, sig: str, slot: int,
              tx_index: int, venue: str | None) -> None:
        self.last_activity_time = t
        if venue:
            self.venues.add(venue)
        if kind == "swap":
            if token_delta > 0:
                cost = -sol_lamports
                self.qty += token_delta
                self.cost += cost
                self.bought_qty += token_delta
                self.bought_sol += cost
                self.n_buys += 1
                if self.first_buy_time is None:
                    self.first_buy_time = t
                    self.first_buy_sig = sig
                    self.first_buy_slot = slot
                    self.first_buy_tx_index = tx_index
                    self.first_buy_sol = cost
                    self.first_buy_qty = token_delta
            else:
                q = -token_delta
                proceeds = sol_lamports
                known = min(q, max(self.qty, 0))
                basis = (self.cost / self.qty * known) if self.qty > 0 else 0.0
                self.realized += proceeds - basis
                self.cost -= basis
                self.qty -= known
                self.sold_no_basis_qty += q - known
                self.sold_qty += q
                self.sold_sol += proceeds
                self.n_sells += 1
                if self.first_sell_time is None:
                    self.first_sell_time = t
                self.last_sell_time = t
        elif kind in ("lp_add", "lp_remove"):
            # une position de liquidité n'est pas une vente : elle sort du stock sans réalisé, signalée
            if token_delta < 0:
                q = -token_delta
                known = min(q, max(self.qty, 0))
                if self.qty > 0:
                    self.cost -= self.cost / self.qty * known
                self.qty -= known
                self.lp_token_in += q
            else:
                self.qty += token_delta
                self.lp_token_out += token_delta
            if sol_lamports < 0:
                self.lp_sol_in += -sol_lamports
            else:
                self.lp_sol_out += sol_lamports
        elif kind in ("transfer", "fee_share"):
            self.n_transfers += 1
            if token_delta > 0:
                self.qty += token_delta
                self.transfer_in_qty += token_delta
            else:
                q = -token_delta
                known = min(q, max(self.qty, 0))
                if self.qty > 0:
                    self.cost -= self.cost / self.qty * known
                self.qty -= known
                self.transfer_out_qty += q

    @property
    def completeness(self) -> str:
        if self.lp_token_in or self.lp_sol_in or self.lp_token_out or self.lp_sol_out:
            return "partiel: positions de liquidité"
        if self.sold_no_basis_qty > 0:
            return "partiel: ventes sans quantité connue"
        if self.transfer_in_qty > 0:
            return "partiel: jetons reçus sans coût"
        if self.transfer_out_qty > 0:
            return "partiel: jetons sortis hors swap"
        return "complet sur le pool et la courbe"
