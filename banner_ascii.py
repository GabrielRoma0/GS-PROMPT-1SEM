# banner_ascii.py
# Script auxiliar para testar e visualizar fontes ASCII
# Uso: python banner_ascii.py

import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

linha1 = pyfiglet.figlet_format("ConnectSat", font="ansi_shadow")
linha2 = pyfiglet.figlet_format("Mission Control AI", font="small")

console.print(Align.center(Text(linha1, style="bold #06B6D4")))
console.print(Align.center(Text(linha2, style="bold #A855F7")))
console.print(Align.center(
    Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
         style="italic #8484A0")
))