"""Collecte complète (transactions jsonParsed) des courbes Pump.fun de KM et KEKIUS-XC78 jusqu'au 04/01/2025."""
from k_lib import KM_CURVE, XC_CURVE, T_END
from dmaga.collect import collect, verify
from dmaga.helius import Helius

h = Helius(rps=5)
for label, a in [("km_curve", KM_CURVE), ("xc_curve", XC_CURVE)]:
    st = collect(h, label, a, details="full", limit=100, filters={"blockTime": {"lt": T_END}}, log=print)
    print(label, st["n"], verify(label))
print(dict(h.stats))
