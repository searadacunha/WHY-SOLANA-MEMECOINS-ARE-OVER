# GRAPHS — graphe organisationnel (séparé du graphe financier)

Le graphe financier se trouve dans `FINANCIAL_BENEFICIARIES.md` § 3. Les deux graphes ne sont reliés que par **une seule** arête, en pointillés : DMC ↔ wallet créateur, niveau B (image commune et publication du CA). Ce n'est pas une preuve de contrôle.

```mermaid
flowchart TB
  DMC["@DarkMagaCoin<br/>communication officielle<br/>CA 02:26:35 (A)"]
  MUR["@Murray_Gothbard (ex-@ChristienPhoto)<br/>artiste / promoteur<br/>visuel $DMAGA 02:31:29 (A)"]
  KIK["@kikisknees<br/>communication / artiste<br/>RT du CA 02:45:55 (A)"]
  WIN["@ChrisWinig<br/>artiste, pfp (B)"]
  KAN["@kanpai<br/>« lead » déclaré (C)"]
  ESO["@Esoviz<br/>« media team lead » 13/08 (C)"]
  COC["@CryptoOnlyCoims<br/>promoteur indépendant (A post)"]
  KJ["@koreanjewcrypto<br/>promoteur (C)"]
  ARI["@Aristos_Revenge<br/>protégé (D)"]
  RT["5 relais RT de Murray<br/>Official67Token, SpecialBea99061, BoredNap66757, Jacwin_n, Fudrap96"]
  KIK -->|RT 02:45:55| DMC
  KIK -.->|« pfp by me and @ChrisWinig » C| WIN
  DMC -.->|« media team lead » 13/08 C| ESO
  MUR -.->|« my friend developed the token » C| DMC
  RT -->|RT 02:44–02:49| MUR
  COC -->|réponse 02:48:08| DMC
  KAN -.->|déclaration C| DMC
  W8["wallet 8YLEuU… (créateur)"]
  DMC -.->|B : même image + 1er à publier le CA| W8
```

## Classements (rappel)

1. **Promoteurs, par heure de publication** : `EARLIEST_PROMOTERS.md`. Ordre : DMC 02:26:35 → Murray 02:31:29 → adamjia7 02:33:53 → Official67Token 02:44:08 → SpecialBea99061 02:45:49 → kikisknees 02:45:55 → BoredNap66757 02:46:00 → Jacwin_n 02:46:16 → eseleo 02:46:33 → CryptoOnlyCoims 02:48:08.
2. **Acheteurs, par premier achat réussi** : `FIRST_BUYERS.md` § 3 (20 premiers + créateur).
3. **Bénéficiaires, par profit réalisé** : `FINANCIAL_BENEFICIARIES.md` § 1.
