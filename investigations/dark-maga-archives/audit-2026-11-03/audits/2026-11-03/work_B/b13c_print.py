import pandas as pd
from pathlib import Path
H=Path(__file__).parent
d=pd.read_csv(H/"b13_scenarios.csv")
print(d[["scenario","taux_verdict_inhabituel","p_min_median","SOL_sur_DMAGA","DMAGA_passe","p_DMAGA"]].round(4).to_string())
t=pd.read_csv(H/"b11_dmaga_table.csv")
print(t[["mesure","D_etude","D_B","med_pairs","p90","max_pairs","c","p","rang_sur_212","percentile","q_IC95_bas","q_IC95_haut","facteur_pour_depasser_max"]].round(4).to_string())
