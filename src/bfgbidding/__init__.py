"""Expose the classes in the API."""

from ._version import __version__
from .bidding import Bid, Double, Pass
from .comments import comment_xrefs, comments, convert_text_to_html, strategies
from .hand import Hand
from .player import Player
from .strategy_xref import StrategyXref, strategy_descriptions
from .utils import get_role

VERSION = __version__
