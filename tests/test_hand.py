
from bfgbidding.hand import Hand


def test_double_allowed():
    hand = Hand()

    # One bid
    hand.bid_history = ['P']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C']
    assert hand.double_allowed() is True

    # Two bids
    hand.bid_history = ['P', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['P', '1C']
    assert hand.double_allowed() is True

    hand.bid_history = ['1C', '1D']
    assert hand.double_allowed() is True

    hand.bid_history = ['1C', 'D']
    assert hand.double_allowed() is False

    # Three bids
    hand.bid_history = ['P', 'P', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C', 'P', 'P']
    assert hand.double_allowed() is True

    hand.bid_history = ['P', '1C', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['P', 'P', '1C']
    assert hand.double_allowed() is True

    hand.bid_history = ['1C', '1D', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C', 'D', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C', 'P', '1D']
    assert hand.double_allowed() is True

    hand.bid_history = ['P', '1C', '1D']
    assert hand.double_allowed() is True

    hand.bid_history = ['P', '1C', 'D']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C', 'D', 'P']
    assert hand.double_allowed() is False

    hand.bid_history = ['1C', '1D', 'D']
    assert hand.double_allowed() is False


def test_redouble_allowed():
    hand = Hand()

    # One bid
    hand.bid_history = ['P']
    assert hand.redouble_allowed() is False

    # Two bids
    hand.bid_history = ['1C', 'D']
    assert hand.redouble_allowed() is True

    hand.bid_history = ['1C', '1D']
    assert hand.redouble_allowed() is False

    # Three bids
    hand.bid_history = ['1C', '1D', 'D']
    assert hand.redouble_allowed() is True

    hand.bid_history = ['1C', '1D', '1H']
    assert hand.redouble_allowed() is False

    hand.bid_history = ['1C', '1D', 'D', 'P', 'P']
    assert hand.redouble_allowed() is True
