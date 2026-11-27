import pandas as pd
from pathlib import Path
d=pd.read_csv(Path(__file__).with_name("b01_peak.csv"))
out=[]
out.append(("tokens",len(d)))
out.append(("hist_non_vide",(d.hist_hours>0).sum()))
out.append(("tronques",d.truncated.sum()))
out.append(("n_late<500 et hist_vide",((d.n_late_first_page<500)&(d.hist_hours==0)).sum()))
out.append(("n_late>=500 et hist_vide",((d.n_late_first_page>=500)&(d.hist_hours==0)).sum()))
out.append(("n_late<500 et hist_non_vide",((d.n_late_first_page<500)&(d.hist_hours>0)).sum()))
out.append(("S20",d.S20.notna().sum()))
out.append(("S10",d.S10.notna().sum()))
out.append(("tronques_S20",((d.truncated==1)&d.S20.notna()).sum()))
out.append(("tronques_sans_S20",((d.truncated==1)&d.S20.isna()).sum()))
out.append(("tronques_sans_S20_ni_S10",((d.truncated==1)&d.S20.isna()&d.S10.isna()).sum()))
out.append(("non_tronques_S20",((d.truncated==0)&d.S20.notna()).sum()))
for k,v in out: print(k,v)
print(d[d.mint=="7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump"].T)
import os
EXT="/Volumes/VERBATIM HD/Dark-MAGA-Investigation/raw/ctrl_tx"
dirs=[x for x in os.listdir(EXT) if not x.startswith("._")]
print("dirs",len(dirs))
s=set(dirs); dd=d[d.pool.isin(s)]
print("dirs in activity",len(dd),"avec S20",dd.S20.notna().sum(),"avec S10",dd.S10.notna().sum(), "tronq",dd.truncated.sum())
print("dirs not in activity", [x for x in dirs if x not in set(d.pool)][:10])
