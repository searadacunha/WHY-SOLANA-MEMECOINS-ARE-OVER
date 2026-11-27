"""Nombres à la française dans un texte Markdown, sauf entre accents graves (adresses, chemins, signatures)."""
import re

_THOUS = re.compile(r"(?<![\w.,/:])(?<!\d-)([1-9]\d{0,2}(?:,\d{3})+)(\.\d+)?(?![\w/:])")  # 0,032 est déjà un décimal français
_DEC = re.compile(r"(?<![\w.,/:])(?<!\d-)(\d+)\.(\d+)(?![\w/:]|\.\d)")


def fr(text: str) -> str:
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        s = _THOUS.sub(lambda m: m.group(1).replace(",", " ") + (m.group(2) or ""), parts[i])
        parts[i] = _DEC.sub(lambda m: f"{m.group(1)},{m.group(2)}", s)
    return "`".join(parts)


if __name__ == "__main__":
    assert fr("0,032 SOL") == "0,032 SOL"
    assert fr("-1,234.5 et -42.5, 07:57-08:33") == "-1 234,5 et -42,5, 07:57-08:33"
    assert fr("5,491 SOL et 0.032 SOL, `H3.x,123` 21/07 19:03:27 1,234.5") == "5 491 SOL et 0,032 SOL, `H3.x,123` 21/07 19:03:27 1 234,5"
