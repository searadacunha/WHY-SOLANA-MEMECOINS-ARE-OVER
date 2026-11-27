"""Read DLN order IDs only from successful Solana executions of the DLN program.

An Order Id printed by another invoked program is not a DLN event. Source
CreatedOrderId uses the Anchor discriminator sha256('event:CreatedOrderId')[:8].
No network or third-party dependencies.
"""
import base64
import hashlib
import re

SOURCE = "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4"
DESTINATION = "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo"
CREATED_ID = hashlib.sha256(b"event:CreatedOrderId").digest()[:8]
INVOKE = re.compile(r"Program (\w+) invoke \[(\d+)\]")
END = re.compile(r"Program (\w+) (success|failed:.*)")
ORDER_ID = re.compile(r"Program log: Order Id:\s*(0x[0-9a-fA-F]{64}|[0-9]+)")


def order_ids(tx, program):
    meta = tx.get("meta") or {}
    if "err" not in meta or meta["err"] is not None:
        return set()
    stack, found = [], set()
    for line in meta.get("logMessages") or []:
        hit = INVOKE.fullmatch(line)
        if hit:
            depth = int(hit[2])
            if depth != len(stack) + 1:
                raise ValueError("Inconsistent Solana invocation depth")
            stack.append((hit[1], set()))
            continue
        hit = END.fullmatch(line)
        if hit:
            if not stack or stack[-1][0] != hit[1]:
                raise ValueError("Inconsistent Solana program completion")
            _, events = stack.pop()
            if hit[2] == "success":
                (stack[-1][1] if stack else found).update(events)
            continue
        if not stack or stack[-1][0] != program:
            continue
        if program == DESTINATION and (hit := ORDER_ID.fullmatch(line)):
            value = int(hit[1], 16 if hit[1].startswith("0x") else 10)
            if value >= 1 << 256:
                raise ValueError("Solana order ID exceeds bytes32")
            stack[-1][1].add("0x%064x" % value)
        if program == SOURCE and line.startswith("Program data: "):
            data = base64.b64decode(line[14:], validate=True)
            if data.startswith(CREATED_ID):
                if len(data) != 40:
                    raise ValueError("Truncated CreatedOrderId event")
                stack[-1][1].add("0x" + data[8:].hex())
    if stack:
        raise ValueError("Incomplete Solana program logs")
    return found
