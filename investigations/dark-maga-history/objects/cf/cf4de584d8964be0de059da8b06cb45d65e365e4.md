# Graphe des principaux flux (06/11/2026, version auditée)

Flèches pleines : transactions relues sur la chaîne (deBridge relié par orderId recalculé). Pointillés : relation EXPLORATORY ou mélange non borné. Heures UTC.

```mermaid
flowchart LR
  subgraph ETH["Ethereum"]
    B947["b947 0xb947…8c57"] -->|"334 291 USDC 01/10/2024"| REL["relais 0x4978…c04d"]
    B298E["b298 0xb298…fa67"] -->|"100 000 USDC 06/10 19:28 (non marqué au pire cas)"| REL
    REL -->|"434 291 USDC, tout vers b298"| B298E
  end
  subgraph BASE["Base"]
    B298B["b298 (Base)"]
    CBD["0x34172888… dépôt Coinbase"] --> CB14["Coinbase 14"]
    ZX["0x2ac17414… satellite"]
    BLO["0xb1e5042f… dépôt BloFin (Ethereum)"]
  end
  subgraph BSC["BSC"]
    B298S["b298 (BSC)"]
  end
  subgraph SOL["Solana"]
    EI5["Ei5yGz8d…"]
    GV2["GV2w4YvX… (neuf)"] -->|"182 548,80 USDC 13/11"| MXD["96W8V3to… dépôt MEXC"] --> MEXC["MEXC 1 ASTyfSima4…"]
    CB3["Coinbase GJRs4FwH…"] -->|"2,25 Md BONK 12/11"| EI5
    EI5 -->|"5,02 Md BONK 12/11"| GV2
    EI5 -->|"DCA 482 SOL → FvgqHM, tout le 18/11"| AE["2aeEoq5n… (neuf)"]
    AE -->|"vente 393,81 SOL 20/11, réinvestie"| AE
    EI5 -->|"1,55 SOL 08/04/2024"| D39["39dTXaMM… dépôt Coinbase"]
    HP2["Hp2BtvnZ…"] -->|"3,27 SOL 07/05/2024"| D39
    HP2 -->|"1,013 SOL 13/05/2024"| EI5
    D39 --> CB1["Coinbase 1 et 3"]
    K8["8kNKNiHK… / BdX9J5pQ…"] -->|"289,03 SOL 23/07/2024"| EI5
  end
  B298E -->|"o1 : 100 048,9 USDC → 29,74 ETH 12/11 01:44"| B298B
  B298B -->|"24 ETH 08:57 (b947 : ≥ 23,75 sous H)"| CBD
  B298E -->|"o2 : 99 989,8 USDC → 157,37 BNB 17:42"| B298S
  B298S -->|"29,845 ETH 17:53"| B298E
  B298E -->|"29,02 ETH → 445,50 SOL 21:26"| EI5
  B298E -->|"482,63 SOL 17/11"| EI5
  EI5 -->|"2 ordres 26/11"| ZX
  ZX -->|"0,16 ETH 27/11"| B298B
  B298B -->|"7,0 ETH → 23 882,89 USDT 27/11"| BLO
  B298B -.->|"6 ordres → USDT (part b947 non bornée)"| MXE["0x311ef6b5… dépôt MEXC (Ethereum)"]
  CBD -.->|"même jour, valeur comparable, non prouvé"| CB3
```

Lecture de la frontière (`FINDINGS.md` §3) : o1 et o2 portent ensemble au moins 100 028,64 USDC de b947. La répartition entre la branche Coinbase et la branche MEXC dépend de la règle d'allocation au relais.
