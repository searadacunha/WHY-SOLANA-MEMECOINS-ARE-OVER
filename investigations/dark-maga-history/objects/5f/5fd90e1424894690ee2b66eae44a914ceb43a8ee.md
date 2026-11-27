# Reprise : bénéficiaires, créations et répétitions de transferts

État initial vérifié le 6 novembre 2026. Ce dossier est distinct des corrections de provenance et du décodeur DLN de la PR #17.

- Base de travail : `main`, `0f77f26f5be09e42453ae2769e5e0ad67ed39a7c`.
- PR #15 et #16 fusionnées ; PR #17 ouverte, HEAD observé `7a3d3fc9c673ffc3a91e8bfbcaaadeeea6c501b6`. Ses corrections ne sont pas présentées comme nouvelles ici. La PR #1 reste draft.
- Branche dédiée : `investigation/creator-links-pump-detection-20261106`.
- Les archives externes mentionnées dans `state/STATE.md` ne sont pas montées. Les données publiées comprennent des grands livres dérivés et des transactions brutes sélectionnées ; leur présence ne rend pas possible un replay intégral des collectes.
- Aucun accès au pool de clés Helius n'est présumé. La collecte complémentaire doit conserver requêtes publiques, réponses, horodatages, empreintes et limites de couverture.
- README racine et études gelées conservés. Aucune opération de trading, signature ou transfert.

## Périmètre

1. Réparer la détection Pump.fun de `s32_recipients.py` et tester son attribution. Le test historique `"create" in ...[:0]` est toujours faux. L'initialisation SPL d'un mint ne suffit pas à démontrer que le payeur de la transaction est son créateur Pump.fun.
2. Vérifier les créations associées à `B5fC3Dg42BRT8GffXg8nPy6ktQtgQ1UL5pHTZ7rnsmmR`, bénéficiaire de 3,35 SOL d'Ei5 le 7 octobre 2024. Les créations signalées sont antérieures, en juin : ce versement ne prouve pas leur financement.
3. Examiner les transferts directs d'autres jetons entre les wallets déjà étudiés, et les sources de financement des séquences de création. Les résultats calculés sur CSV restent explicitement distincts des transactions brutes revérifiées.
4. Auditer des outils GitHub par lecture du code, licence et compatibilité historique avant toute intégration.

## Contrôles initiaux

Sur le HEAD de base : validateur deBridge et 15 tests réussis ; 12 tests hors ligne Base/BSC/Solana et 31 assertions de son selfcheck réussis ; 31 contrôles du selfcheck EVM réussis depuis son répertoire `scripts` ; 14 tests du garde de publication réussis. Le garde `--target main` préserve le README et les 17 fichiers gelés. Ces résultats ne valident pas des conclusions nouvelles.

Le selfcheck EVM historique dépend du répertoire courant et échoue depuis la racine du dépôt ; l'invocation depuis son dossier fonctionne. Les anciennes bornes conditionnelles sous H restent conditionnelles, même si ce selfcheck réussit. Ne pas les transformer en bornes inconditionnelles.

## Interprétation

Un transfert financier exact ne démontre pas une identité civile, une propriété commune des clés, une manipulation de marché ou une connaissance préalable d'une décision d'Elon Musk. Un taux observé dans ces wallets sélectionnés ne constitue pas un taux de base indépendant.
