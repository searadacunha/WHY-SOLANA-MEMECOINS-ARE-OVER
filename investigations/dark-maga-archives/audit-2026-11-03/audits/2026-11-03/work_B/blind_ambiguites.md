# Ambiguïtés du plan et choix de l'auditeur B, notés à l'aveugle (avant le sceau)

Sources lues à ce stade : `etude_final/analysis_plan.md`, `AGENTS.md`, `dmaga/config.py`, données brutes.

| id | Passage du plan | Lectures possibles | Choix B | Mesures touchées |
|----|---|---|---|---|
| A01 | « heure h », « début de la première heure » | heure UTC alignée, ou heure relative à la création | UTC alignée (clé `hist` = epoch // 3600) | S |
| A02 | h ≥ création + 96 h | début de h, ou heure qui contient l'instant | début de h ≥ création + 96 h, début de h < création + 60 j | S |
| A03 | médiane des 72 heures précédentes | heures absentes de `hist` = 0, ou ignorées | absentes = 0 ; moyenne des 2 valeurs centrales | S |
| A04 | pool tronqué, dernière heure partielle | valide ou non comme pic | valide si elle passe le seuil (le vrai n est plus grand) | S |
| A05 | « en USD à la minute » | minute de S−1 h ou du dernier swap ; open ou close | close de la minute de S−1 h | filtre cap |
| A06 | « Dernier swap lu » | swap au sens des vaults, ou avec bénéficiaire retenu | variation opposée des vaults, sans exiger de bénéficiaire | filtre cap |
| A07 | « parmi les 200 dernières transactions » | toutes les tx du pool, ou celles qui touchent le vault | rang compté sur les tx qui touchent le vault SOL | `sans_swap_avant_S` |
| A08 | « parts sous 5 % du swap » | part de la variation du vault, ou de la somme des owners | \|delta owner\| / \|dT du vault\| | toutes |
| A09 | SOL attribué à un bénéficiaire | part × \|dS\|, ou tout \|dS\| au bénéficiaire, ou normalisé sur les retenus | part × \|dS\|, part plafonnée (somme > 1 ramenée à 1), sans renormaliser quand des parts sont écartées | M1 à M4, M7 |
| A10 | « lignes de swap » | une par transaction, ou une par (transaction, bénéficiaire) | une par (transaction, bénéficiaire retenu) | filtre 20 swaps |
| A11 | « autre mint » pour le non-signataire | WSOL et autres jetons, SOL natif ou non | soldes de jetons seulement (WSOL inclus), pas le SOL natif | toutes |
| A12 | M1 « fenêtre glissante [...] sans chevauchement » | contradictoire : glissante et sans chevauchement | fenêtres contiguës ancrées à S−75 h, 24 fenêtres, vides = 0 | M1 |
| A13 | M2 médiane par fenêtre de 24 h | 3 fenêtres seulement | 3 fenêtres contiguës, vides = 0 | M2 |
| A14 | M3 « sans aucun swap Raydium antérieur » | antérieur à la fenêtre, ou à chaque achat | premier swap (achat ou vente) ≥ S−24 h : tous ses achats de la fenêtre comptent. Variante M3b : seul le premier achat | M3 |
| A15 | M5 « 216 000 slots » | constante, ou slots réels de la fenêtre | constante du plan | M5 |
| A16 | M6 « part des jetons » | agrégée, ou moyenne par wallet ; ventes > achats | Σ max(0, achetés − vendus) / Σ achetés, agrégée. Variante M6b : moyenne par wallet | M6 |
| A17 | M6 « achetés avant S » | achats des précoces jusqu'à S, ou seulement ceux des 24 h | tous les achats des précoces jusqu'à S | M6 |
| A18 | M7 « plus gros achat unique, rapporté à la réserve » | plus gros en SOL puis ratio, ou plus grand ratio ; ligne ou transaction | plus gros en SOL par ligne, puis ratio. Variante M7b : ratio maximal | M7 |
| A19 | M7 « réserve juste avant lui » | solde pre de la transaction | `pre` du vault WSOL dans la même transaction | M7 |
| A20 | ordre filtres et chaîne de soldes | pool rompu exclu avant ou après la bande | chaîne appliquée après les 4 conditions, comptée à part | population |
| A21 | chaîne de soldes | WSOL seul (plan) | WSOL fait foi, vault jeton compté en plus | population |
| A22 | k et p | DMAGA dans k ou non | k = comparateurs sans DMAGA, p = (1 + #{comp ≥ D}) / (k + 1), NaN hors du rang | tests |

## Limites vues à l'aveugle
- La capitalisation à S−1 h et le filtre 20 swaps ne se recalculent depuis le brut que pour les pools présents dans `raw/ctrl_tx` (249 dossiers sur 954 tokens ayant un S20). Pour les autres, aucun brut sur le disque. Je ne peux pas recalculer la population complète sans lire `selection.jsonl`.
- 4 curseurs `ctrl_tx` ont `complete: false` (`5jG2h6zF...`, `8deVHU54...`, `EUr4qeHV...`, `acaDbR5Q...`, voir `b02b_cursors.csv`). Le détail de leur effet est à vérifier.
