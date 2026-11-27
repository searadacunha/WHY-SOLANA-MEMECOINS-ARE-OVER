import pandas as pd
from pathlib import Path
H=Path(__file__).parent
d=pd.read_csv(H/"b13_scenarios.csv")
for _,r in d[d.scenario.isin(["0.25R_1w_3h","1R_1w_3h","2R_1w_3h","5R_1w_3h","1R_5w_24h","2R_25w_24h_sync","controle_moyen_6w_60SOL_3h_sync","controle_fort_18w_740SOL_3h_sync"])].iterrows():
    print(r.scenario, r.taux_verdict_inhabituel, r.SOL_sur_DMAGA, r.M_DMAGA, r.p_DMAGA, r.DMAGA_passe, "|", r.passe_M1,r.passe_M2,r.passe_M3,r.passe_M4,r.passe_M5,r.passe_M6,r.passe_M7)
print(pd.read_csv(H/"b13_facteurs.csv").round(3).to_string())
