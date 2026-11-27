"""Pure point-in-time predicates for historical token-rotation screens.

A debit in another token after the first DMAGA buy must never be counted as
evidence of a pre-buy rotation. This helper does not determine whether the
debit was a genuine DEX sale; transaction semantics must be audited separately.
"""


def in_prebuy_window(event_time: int, first_buy_time: int, lookback_seconds: int = 3600) -> bool:
    """True exactly for t_first_buy - lookback <= t_event < t_first_buy."""
    if lookback_seconds <= 0:
        raise ValueError("lookback_seconds must be positive")
    return first_buy_time - lookback_seconds <= event_time < first_buy_time
