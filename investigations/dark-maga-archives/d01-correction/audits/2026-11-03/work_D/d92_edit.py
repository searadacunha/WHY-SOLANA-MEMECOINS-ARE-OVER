p='AUDIT_FINAL.md'; s=open(p,encoding='utf-8').read()
rep=[("Compatible. Les transferts de 24 h sont internes au groupe à 96 % en réception","Compatible. Sur les 114,96 M reçus en 24 h, 110,2 M le sont par des membres du groupe, soit 96 %"),
("centile moyen 0,755, p 0,0425 exploratoire, sur plus de 121 comparaisons de B, sans valeur de preuve","centile moyen 0,755, p 0,0425 exploratoire, une comparaison parmi les 121 de B, sans valeur de preuve"),
("3 wallets à 0,75 SOL en 2 min 25 s le 26/06/2024, 2 wallets à 0,02 SOL le 23/08/2024. L'habitude précède le mint de 18 jours (N15).","3 wallets à environ 0,75 SOL en 2 min 25 s le 26/06/2024, 2 wallets à 0,02 SOL le 23/08/2024. L'habitude précède le mint de 17 jours (N15)."),
("| C15, part du groupe | 2,3746 % | 2,375 % | +0,0003 point | `d43_perim.py` |","| C15, part du groupe | 2,3746 % | 2,3749 % | +0,0002 point | `d43_perim.py` |"),
("Wallets non tracés à écart d'au moins 1 M : 0 avant Musk, 0 sur 24 h, 102 ensuite pour 274,4 M.","Ruptures d'au moins 1 M sur des wallets non tracés : 0 avant Musk, 0 sur 24 h, 102 ensuite pour 274,4 M."),
]
for a,b in rep:
    assert s.count(a)==1,a
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
p='work_D/d90_make_claims.py'; s=open(p,encoding='utf-8').read()
a="G9uiJWzsPUoDuZKXEWSBvEtCi5NtU6iCQc6SeBPSRScT à 0,75 SOL"; assert s.count(a)==1
s=s.replace(a,"G9uiJWzsPUoDuZKXEWSBvEtCi5NtU6iCQc6SeBPSRScT à 0,75 ; 0,75 ; 0,7496 SOL")
open(p,'w',encoding='utf-8').write(s)
