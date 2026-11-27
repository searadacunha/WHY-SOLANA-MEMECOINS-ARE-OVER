for p, a, b in (("AUDIT_FINAL.md", "A-12 (5 001 lignes, 3 wallets, sans effet sur C37)", "A-12 (les 5 000 lignes de A retrouvées, mon filtre en voit 5 001 sur 3 wallets, sans effet sur C37)"),
                ("CORRECTIONS.md", "`d48_exits.txt` : 5 001 lignes, 3 wallets, sans effet sur C37", "`d48_exits.txt` : 5 001 lignes au-dessus de 100 000 SOL, 3 wallets, sans effet sur C37")):
    s = open(p, encoding="utf-8").read(); assert s.count(a) == 1; open(p, "w", encoding="utf-8").write(s.replace(a, b))
