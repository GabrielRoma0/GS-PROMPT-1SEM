# main.py
# Ponto de entrada da Mission Control AI — ConnectSat
"""Mission Control AI — ConnectSat · FIAP Global Solution 2026.1"""

from src.ui import run_cli
from src.engine import MissionEngine

if __name__ == "__main__":
    engine = MissionEngine()
    run_cli(engine)