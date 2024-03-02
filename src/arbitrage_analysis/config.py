"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

THE_ODDS_API_API_KEY = "6c335dcec08f7534db180f97b29e4d92"

__all__ = ["BLD", "SRC", "TEST_DIR", "GROUPS"]