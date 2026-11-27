import csv
for r in csv.DictReader(open('REDACTED_HOME/Projects/Dark-MAGA-Investigation/audits/2026-11-03/work_C/counterparties.csv')):
    if int(r['lamports'])>=5e7 or r['label'] :
        print(r['seed'][:6],r['dir'],r['counterparty'],r['n'],round(int(r['lamports'])/1e9,4),'L:'+r['label'][:30] if r['label'] else '', 'ATA:'+r['ata_mint'][:8] if r['ata_of_seed']=='True' else '')
