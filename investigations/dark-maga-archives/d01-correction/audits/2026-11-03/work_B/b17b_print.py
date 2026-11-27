import pandas as pd
from pathlib import Path
H=Path(__file__).parent
d=pd.read_csv(H/"b10_diff_tokens.csv")
for m,g in d.groupby("mesure"):
    print(g.head(4)[["mesure","pool","etude","B","rel","n_buyers","n_buyers_B"]].to_string(header=False))
