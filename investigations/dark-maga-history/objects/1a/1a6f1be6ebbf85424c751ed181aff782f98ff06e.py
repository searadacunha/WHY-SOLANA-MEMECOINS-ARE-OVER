"""Regression: never decode a similarly-shaped log as a deBridge order without matching topic0."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dln


def word(n):
    return "0x" + n.to_bytes(32, "big").hex()


def created_payload():
    # ABI: 7-word event head, 14-word Order tuple, one empty dynamic-bytes tail.
    # All dynamic fields point to the same valid empty bytes value.
    heads = [7 * 32, 123, 0, 500, 70, 0, 0]
    fields = [5, 14 * 32, 1, 14 * 32, 1_000_000, 8453, 14 * 32,
              990_000, 14 * 32, 14 * 32, 14 * 32, 14 * 32, 14 * 32, 14 * 32]
    return "0x" + "".join(n.to_bytes(32, "big").hex() for n in heads + fields + [0])


def log(address, topic, data):
    return {"address": address, "topics": [topic], "data": data, "logIndex": "0x0"}


class TestDeBridgeTopics(unittest.TestCase):
    def test_fulfilled_version_requires_full_topic(self):
        a = log(dln.DLN_DST, dln.FULFILLED, "0x")
        b = log(dln.DLN_DST, dln.FULFILLED_V2, "0x")
        self.assertEqual(dln.fulfilled_version(a), 1)
        self.assertEqual(dln.fulfilled_version(b), 2)
        a["topics"] = [dln.FULFILLED[:18] + ("0" * 48)]
        b["topics"] = [dln.FULFILLED_V2[:18] + ("0" * 48)]
        self.assertEqual(dln.fulfilled_version(a), 0)
        self.assertEqual(dln.fulfilled_version(b), 0)
        self.assertEqual(dln.fulfilled_version(log("0x" + "0" * 40, dln.FULFILLED, "0x")), 0)

    def test_created_order_requires_exact_event_and_source(self):
        data = created_payload()
        good = log(dln.DLN_SRC_EVM, dln.CREATED_ORDER, data)
        tx = {"transactionHash": "0x" + "0" * 64, "logs": [good]}
        orders = dln.created_in_receipt(tx)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["giveChainId"], 1)
        self.assertEqual(orders[0]["takeChainId"], 8453)
        self.assertEqual(orders[0]["nativeFixFee"], 500)
        self.assertEqual(orders[0]["orderId"], word(123))

        # Previously the same payload could be interpreted as an order under
        # an unrelated event topic from the very same DlnSource contract.
        tx["logs"] = [log(dln.DLN_SRC_EVM, "0x" + "a" * 64, data),
                      log(dln.DLN_SRC_EVM, dln.FULFILLED, data),
                      log("0x" + "0" * 40, dln.CREATED_ORDER, data),
                      log(dln.DLN_SRC_EVM, dln.CREATED_ORDER[:18] + ("0" * 48), data)]
        self.assertEqual(dln.created_in_receipt(tx), [])


if __name__ == "__main__":
    unittest.main()
