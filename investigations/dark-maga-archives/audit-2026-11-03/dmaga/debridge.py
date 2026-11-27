"""Accounting over the archived, decoded deBridge source orders (no network).

Amounts in work_I/i14_orders.csv are integer USDC base units.  ``fee_pct`` is
already an amount, not a percentage; native SOL fees have a different unit.
The initiating wallet is ``maker``.  ``wallet_file`` only identifies the cache
in which the transaction was found and must not define a wallet cohort.
"""
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


USDC_SOLANA = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
SOLANA_CHAIN = 7565164
SOURCE_TABLE = "audits/2026-11-03/work_I/i14_orders.csv"
_REQUIRED = {
    "utc", "sig", "nonce", "maker", "give_token", "give_amount",
    "fee_pct", "fee_fix_lamports", "give_chain", "take_chain", "receiver",
}


@dataclass(frozen=True)
class SourceOrder:
    signature: str
    nonce: int
    maker: str
    utc: datetime
    give_amount: int
    proportional_fee: int
    fixed_fee_lamports: int
    take_chain: int
    receiver: str


def _uint(row, name, line):
    value = row[name]
    if not value or not value.isascii() or not value.isdecimal():
        raise ValueError(f"line {line}: {name} must be a non-negative integer")
    return int(value)


def read_decoded_orders(path: Path) -> list[SourceOrder]:
    """Read the I table, failing on missing data, mixed units or repeated events.

    This checks the committed table's accounting inputs. It does not decode raw
    transactions again or establish execution on the destination chain.
    """
    orders = []
    seen = set()
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)) or not _REQUIRED.issubset(fields):
            raise ValueError("decoded deBridge table has missing or duplicate columns")
        for line, row in enumerate(reader, start=2):
            if None in row or any(row[key] is None for key in _REQUIRED):
                raise ValueError(f"line {line}: malformed decoded deBridge row")
            if row["give_token"] != USDC_SOLANA or _uint(row, "give_chain", line) != SOLANA_CHAIN:
                raise ValueError(f"line {line}: expected source USDC on Solana")
            if not all(row[key].strip() for key in ("sig", "maker", "receiver")):
                raise ValueError(f"line {line}: missing signature, maker or receiver")
            try:
                utc = datetime.fromisoformat(row["utc"])
            except ValueError as exc:
                raise ValueError(f"line {line}: invalid source timestamp") from exc
            if utc.tzinfo is None:
                raise ValueError(f"line {line}: source timestamp must include its timezone")
            order = SourceOrder(
                signature=row["sig"], nonce=_uint(row, "nonce", line), maker=row["maker"],
                utc=utc.astimezone(timezone.utc), give_amount=_uint(row, "give_amount", line),
                proportional_fee=_uint(row, "fee_pct", line),
                fixed_fee_lamports=_uint(row, "fee_fix_lamports", line),
                take_chain=_uint(row, "take_chain", line), receiver=row["receiver"],
            )
            identity = (order.signature, order.maker, order.nonce)
            if identity in seen:
                raise ValueError(f"line {line}: repeated source order {order.signature}")
            seen.add(identity)
            orders.append(order)
    if not orders:
        raise ValueError("decoded deBridge table is empty")
    return orders


def source_usdc(orders) -> Decimal:
    """Nominal source USDC including proportional fees, excluding fixed SOL fees."""
    micro_usdc = sum(order.give_amount + order.proportional_fee for order in orders)
    return Decimal(micro_usdc) / Decimal(1_000_000)


def select_makers(orders, members, *, before=None) -> list[SourceOrder]:
    """Select actual initiators, optionally strictly before an aware timestamp."""
    if before is not None and before.tzinfo is None:
        raise ValueError("cohort cutoff must include its timezone")
    members = set(members)
    return [order for order in orders if order.maker in members
            and (before is None or order.utc < before)]


def case_bridge_paragraph(orders, members, mint_utc) -> str:
    """Point 9 of CASE_REPORT, shared by the generator and the targeted replay."""
    members = set(members)
    group = select_makers(orders, members)
    early = select_makers(orders, members, before=mint_utc)
    text = (
        "**Ponts : conserver le périmètre des 33 wallets.** "
        f"Le tableau décodé contient {len(orders)} ordres deBridge pour "
        f"{source_usdc(orders):,.2f} USDC nominaux côté source, toutes populations confondues. "
        f"**{len(group)} ordres, {source_usdc(group):,.2f} USDC, ont pour initiateur "
        f"un membre des {len(members)} wallets**, dont {len(early)} ordres pour "
        f"{source_usdc(early):,.2f} USDC avant la création du mint. "
        "Ces sommes incluent les frais proportionnels du pont et excluent les frais fixes en SOL. "
        f"Elles sont recalculées depuis `{SOURCE_TABLE}` et les membres de "
        "`data/prevent_groups.json`, en utilisant `maker`, et non le wallet du fichier de cache. "
        "Le périmètre « P2 » de G diffère de ces 33 wallets. "
        "Ces historiques incluent des opérations hors de la fenêtre Musk et ne mesurent pas "
        "des bénéfices $DMAGA. Dans son périmètre de 76 ordres, la relecture I rapporte "
        "41 exécutions Ethereum associées à 942 534,32 USDC côté source, soit 92,5 % du total ; "
        "35 arrivées restent non vérifiées. Le montant source n'est pas le montant reçu à destination. "
    )
    c73 = select_makers(orders, {"C73Yv9iHmTaf8SU2XFnGLt7QXUDqbeWNtUYza9WJhkae"})
    destination = [o for o in c73 if o.take_chain == 1
                   and o.receiver == "0x2d86499a410a9ac2139833ba8d6942b8a8700a7b"]
    if destination:
        first = min(o.utc for o in destination).strftime("%d/%m/%Y")
        last = max(o.utc for o in destination).strftime("%d/%m/%Y")
        text += (
            f"Les {len(destination)} ordres de `C73Yv9iH…` visant `0x2d86499a…` "
            f"représentent {source_usdc(destination):,.2f} USDC du {first} au {last} "
            f"({len(c73)} ordres et {source_usdc(c73):,.2f} USDC toutes destinations), "
            "pas un seul envoi au lancement. "
        )
    return text + (
        "Sources : relecture H, D01/D28 ; relecture I, section 4. "
        "Recalcul des tables archivées seulement : aucun nouveau décodage du brut, "
        "contrôle d'exécution ou prix USD n'est revendiqué ici."
    )
