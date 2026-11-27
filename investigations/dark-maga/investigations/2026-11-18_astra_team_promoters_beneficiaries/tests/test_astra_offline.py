"""Offline tests for the ASTRA addendum (stdlib only; pytest- and unittest-compatible). No network access."""
import csv, datetime, gzip, hashlib, json, os, sys, tempfile, unittest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import analyze  # noqa: E402
from pumpdecode import summarize  # noqa: E402

MINT = '7D7BRcBYepfi77vxySapmeqRNN1wsBBxnFPJGbH5pump'
G41V = 'G41vRrsHShLEvwMj58ruhqJycGfAtWXxtLD56uFExL8E'
CREATOR = '8YLEuUtZ4eFMJbf46oNb1CeG6dYFWGyxnQSh9hrgzBzR'

def snow(i): return datetime.datetime.fromtimestamp(((i >> 22) + 1288834974657) / 1000, datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def key(name): return json.load(open(os.path.join(ROOT, 'evidence/receipts/key', name + '.json')))['result']
def rcsv(p): return list(csv.DictReader(open(os.path.join(ROOT, p), newline='')))

class Snowflakes(unittest.TestCase):
    CASES = {1812313940841341353: '2024-07-14T02:31:29Z',  # Murray_Gothbard (ex-@ChristienPhoto) "What is happening?!?! Trump rises up."
             1812313858226163712: '2024-07-14T02:31:09Z',  # media key of the $DMAGA laser-eye image in that post
             1812316567150985272: '2024-07-14T02:41:55Z',  # "@pattyice He will rise, higher and stronger $DMAGA"
             1812307129547493658: '2024-07-14T02:04:25Z',  # reply to @KILLARYonSOL, 60 s before the mint
             1812320423373095220: '2024-07-14T02:57:14Z'}
    def test_ids(self):
        for i, t in self.CASES.items(): self.assertEqual(snow(i), t, i)
    def test_murray_post_after_mint_and_before_adamjia7(self):
        self.assertGreater(1812313940841341353, 0)
        self.assertLess(snow(1812313940841341353), '2024-07-14T02:33:53Z')
        self.assertGreater(snow(1812313940841341353), '2024-07-14T02:26:35Z')

class G41vFailedReceipts(unittest.TestCase):
    def check(self, name, slot, limit, amount):
        x = summarize(key(name), MINT)
        self.assertFalse(x['ok']); self.assertEqual(x['error'], 'TooMuchSolRequired'); self.assertEqual(x['signer'], G41V)
        self.assertEqual(x['slot'], slot); self.assertEqual(x['ix'][0]['sol_limit_lamports'], limit); self.assertEqual(x['ix'][0]['token_amount_raw'], amount)
    def test_first(self): self.check('g41v_failed_buy_1_5y7rbp2M', 277417762, 510050000, 14354926048169)
    def test_second(self): self.check('g41v_failed_buy_2_39nfmzR1', 277417795, 408040000, 8008435101172)
    def test_limits_are_ui_rounded(self):
        # 0.5 SOL and 0.4 SOL inputs x 1.01 (fee) x 1.01 (slippage), exactly
        self.assertEqual(round(0.5 * 1.01 * 1.01 * 1e9), 510050000); self.assertEqual(round(0.4 * 1.01 * 1.01 * 1e9), 408040000)

class PumpPhaseRebuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(); analyze.main(cls.tmp)
    def test_rebuild_matches_committed(self):
        a = open(os.path.join(self.tmp, 'pump_phase_txs.csv')).read(); b = open(os.path.join(ROOT, 'data/derived/pump_phase_txs.csv')).read()
        self.assertEqual(a, b)
    def test_counts(self):
        pp = rcsv('data/derived/pump_phase_txs.csv')
        self.assertEqual(len(pp), 436)
        self.assertEqual(sum(r['ok'] == 'False' for r in pp), 181)
        self.assertEqual(sum(r['ok'] == 'True' and r['kind'] == 'buy' for r in pp), 123)
    def test_windows(self):
        w = {r['window']: r for r in rcsv('data/derived/windows_summary.csv')}
        self.assertEqual(w['60s']['failed'], '50'); self.assertEqual(w['60s']['distinct_successful_buyers'], '17')
        self.assertEqual(w['24h']['repo_new_buyers'], '731')
    def test_first_buyers_order_matches_repo_table(self):
        mine = [r['wallet'] for r in rcsv('data/derived/first_buyers_top25.csv')]
        repo = [r['wallet'] for r in sorted(rcsv('data/repo_first1000_buyers_parsed.csv'), key=lambda r: int(r['rank']))][:25]
        self.assertEqual(mine[0], CREATOR)
        self.assertEqual(set(mine), set(repo))  # same 25 wallets
        diffs = [i for i, (a, b) in enumerate(zip(mine, repo)) if a != b]
        self.assertLessEqual(len(diffs), 2)  # only an intra-slot tie may swap
    def test_g41v_attempts(self):
        s = json.load(open(os.path.join(self.tmp, 'sniper_comparison_summary.json')))
        self.assertEqual([a['delay_s'] for a in s['g41v_attempts']], [29, 45]); self.assertEqual([a['slot_delta'] for a in s['g41v_attempts']], [67, 100])
        self.assertEqual(s['first_buy_delay_s_median'], 2); self.assertEqual(s['n_tokens'], 54)

class CoinbaseBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.rows, cls.hits, cls.by = analyze.coinbase_batch()
    def test_four_half_sol_cb3(self):
        b = [r for r in self.rows if r['hot_wallet'] == 'Coinbase 3' and abs(r['sol'] - 0.5) < 1e-12 and '2024-07-14T01:32' <= r['utc'] <= '2024-07-14T01:35']
        self.assertEqual([r['dst'][:8] for r in b], ['8YLEuUtZ', 'GoPCTrS3', 'AFDkwJXJ', 'EEpSRR12'])
        t = [datetime.datetime.strptime(r['utc'], '%Y-%m-%dT%H:%M:%SZ') for r in b]
        self.assertEqual((t[-1] - t[0]).total_seconds(), 112)
    def test_cluster(self):
        self.assertEqual(len(self.rows), 607); self.assertEqual(len(self.hits), 11)
        self.assertEqual(self.by['1.05'], {'all': 5, 'to_9W9b_senders': 5})
        self.assertTrue(all('2024-07-14T01:32:23Z' <= h['utc'] <= '2024-07-14T01:40:50Z' for h in self.hits))

class Integrity(unittest.TestCase):
    def test_sha256sums(self):
        p = os.path.join(ROOT, 'SHA256SUMS.txt')
        if not os.path.exists(p): self.skipTest('SHA256SUMS.txt absent')
        for line in open(p):
            h, f = line.strip().split(None, 1)
            if f.startswith('tests/') or f == 'SHA256SUMS.txt': continue
            self.assertEqual(hashlib.sha256(open(os.path.join(ROOT, f), 'rb').read()).hexdigest(), h, f)
    def test_images(self):
        d = json.load(open(os.path.join(ROOT, 'data/image_comparison.json')))
        self.assertEqual(d['phash_distance']['token|pfp'], 0); self.assertGreater(d['phash_distance']['token|murray_0231'], 20)
        self.assertLess(d['token_vs_pfp_pixels']['share_identical_pixels'], 0.5)  # NOT pixel-identical: re-encoded copy
        h = lambda f: hashlib.sha256(open(os.path.join(ROOT, 'evidence/media', f), 'rb').read()).hexdigest()
        self.assertEqual(h('token_image_ipfs_QmPkBk2.jpg'), '884bdca6ff32245fa4ec21252698f0ade6a1b8546697a30ef196762420f83432')
        self.assertEqual(h('darkmagacoin_pfp_orig.jpg'), '12f965a2db60c5f0236c72eba649a7f895f74b2e2c52d9494aa16ed597469310')

if __name__ == '__main__': unittest.main()
