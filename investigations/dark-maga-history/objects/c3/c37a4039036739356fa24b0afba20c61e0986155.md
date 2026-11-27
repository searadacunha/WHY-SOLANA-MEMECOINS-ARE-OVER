# Graphes de connectivité des flux financiers ($DMAGA)

**Date :** 05/11/2026  
**Légende des liaisons :**
* `==>` : Transfert direct de fonds / jetons sur la même chaîne
* `-.->` : Sortie inter-chaînes (deBridge / DLN)
* `--o` : Dépôt vers un compte collecteur / infrastructure partagée

---

## Graphe 1 : Reconvergence cross-chain vers Ethereum (Sorties deBridge)

Ce schéma montre comment 3 des wallets du groupe des 33 ont fait converger leurs profits en 9 minutes vers la même adresse Ethereum, et comment cette dernière est unifiée à un second compte récepteur depuis septembre 2022.

```mermaid
flowchart TD
    subgraph Solana_Groupe_33["Solana : Membres du Groupe des 33"]
        E["Ei5yGz8d<br/>(223 079 USD bridgés)"]
        G["Gcyg2jeL<br/>(60 460 USD bridgés)"]
        H["HGBiExZR<br/>(157 849 USD bridgés)"]
        C["C73Yv9iH<br/>(527 600 USD bridgés)"]
    end

    subgraph deBridge_Protocol["Protocole deBridge (DLN)"]
        S1["Solveur 0x555ce236..."]
        S2["Solveur 0xe7351fd7..."]
    end

    subgraph Ethereum_Cluster["Ethereum (Mainnet) : Cluster de destination unifié"]
        B9["0xb947bf7f409e998b28f8e218802fc9575c3c8c57<br/>(263 573 USD en 9 min 36 s)"]
        B2["0xb29826d809aa04d2ead6f2310d8965a45b87fa67<br/>(172 578 USD)"]
        AFK["0x2d86499a... (afk.eth)<br/>(496 371 USD en 27 ordres)"]
    end

    G -.->|"Ordres 1 & 2 (60 460 USD)<br/>22/07 00:54 - 00:57 UTC"| S1
    H -.->|"Ordre 1 (156 089 USD)<br/>22/07 01:00 UTC"| S1
    E -.->|"Ordre 1 (47 023 USD)<br/>22/07 01:04 UTC"| S1
    S1 ==>|"Paiement USDC wei-exact"| B9

    E -.->|"15 ordres (170 817 USD)"| S2
    H -.->|"1 ordre (1 760 USD)"| S2
    S2 ==>|"Paiement USDC / ETH"| B2

    B2 ==>|"Financement Gaz (depuis 11/09/2022)"| B9
    B2 ==>|"50 003 USDC (25/07/2024)"| B9

    C -.->|"27 ordres (496 371 USD)"| S2
    S2 ==>|"Exécution vérifiée wei-exact"| AFK
```

---

## Graphe 2 : Le Hub de croisement inter-périmètres `7Gw3gL8m`

Ce schéma détaille l'articulation entre le Périmètre Créateur (P1), le Groupe des 33 et le Top Trader n° 11 via le wallet pivot `7Gw3gL8m`.

```mermaid
flowchart LR
    subgraph P1_Creator["Périmètre Créateur (P1)"]
        D["DfYyxDNE"]
        S6["6ty9DM4s (Série)"]
    end

    subgraph Hub["Wallet Pivot"]
        GW["7Gw3gL8mq7TSENSe..."]
    end

    subgraph G33["Groupe des 33"]
        EG["EGtyQEgM"]
    end

    subgraph Top_Traders["Top Traders Gagnants"]
        TT11["9cfRU5RK<br/>(Rang 11, +729 SOL)"]
    end

    D ==>|"0,70 SOL (15/05/2024)"| GW
    S6 ==>|"1 000 USDC (20/07/2025)"| GW

    GW ==>|"Financement 0,5 SOL (08/02/2024)<br/>+ 4,0 SOL (14/07 02:18 UTC)"| TT11
    TT11 ==>|"Retour 400 SOL<br/>(03/08/2024 04:41:44 UTC)"| GW

    EG ==>|"78,91 SOL<br/>(03/08/2024 04:40:03 UTC)"| GW
    GW ==>|"Renvoi de gaz 1,0 SOL<br/>(03/08 04:40:32 - 29 s après)"| EG
```

---

## Graphe 3 : Les 3 plus gros gagnants et leurs points de convergence

```mermaid
flowchart TD
    subgraph Top_Winners["3 Principaux Gagnants Identifiés"]
        H3["H3QsBrri...<br/>(+5 491 SOL / ~990k USD)"]
        GX["GXZvXsD6...<br/>(+2 540 SOL / ~458k USD)"]
        P9["9PrmF8sf...<br/>(+1 748 SOL / ~317k USD)"]
    end

    subgraph Downstream_H3["Aval H3QsBrri"]
        YS["8YSi5yNR<br/>(Reçoit 2 840 SOL)"]
        BSC["deBridge BSC : 0xfb2ec4e5...<br/>(9 912 USD)"]
    end

    subgraph Downstream_GX["Collecteurs & Relais de GXZvXsD6"]
        C42["42MSVeV4 (Relais 94xmX5J9)"]
        C8N["8N4AvP9j (Balaie MEXC 1)"]
    end

    subgraph Creator_Series_Links["Liaisons avec Série Créateur"]
        ERM["ERMtiLod (Série)"]
        GOP["GoPCTrS3 (Série)"]
        HW["HW5MqvM1"]
        HK["HKzkNSH2"]
    end

    subgraph Downstream_P9["Collecteur 9PrmF8sf"]
        H9X["H9Xezqfd...<br/>(Dépôt Coinbase - 2 051 SOL)"]
        ROT["9 wallets en rotation (2024-2026)"]
    end

    H3 ==>|"2 840 SOL (24-31/07/2024)"| YS
    YS -.->|"deBridge BSC (20/03/2025)"| BSC

    GX ==>|"99,5 SOL + 19,4 SOL + 340,3 SOL"| C42
    GX ==>|"19,7 SOL + 499,1 SOL"| C8N

    ERM ==>|"1,5 M DMAGA (15/07/2024)"| HW
    HW ==>|"95 SOL (25/07/2024)"| C42

    GOP ==>|"1,0 M DMAGA (21/07/2024)"| HK
    HK ==>|"108,8 SOL (30/09 - 01/10/2024)"| C8N

    P9 ==>|"2 051,9 SOL (98,8 % sorties)"| H9X
    ROT --o H9X
```
