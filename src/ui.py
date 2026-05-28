# src/ui.py
# Interface CLI estilo Claude Code — ConnectSat Mission Control AI
# Usa Rich + prompt-toolkit para experiência de terminal moderna

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))


def show_banner():
    """Exibe banner ASCII colorido no início."""
    linha1 = pyfiglet.figlet_format("ConnectSat", font="slant")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="small")

    console.print(Text(linha1, style="bold #06B6D4"))
    console.print(Text(linha2, style="bold #A855F7"))

    console.print(Panel.fit(
        "[bold white]Sistema de monitoramento de satélite LEO de telecomunicações[/]\n"
        "[dim]Conectividade rural · Inclusão digital · Telemedicina · Educação[/]\n\n"
        "[cyan]/help[/] ver comandos  [cyan]/status[/] telemetria  "
        "[cyan]/about[/] sobre  [cyan]/exit[/] sair\n"
        "[dim]Modelo: gpt-oss:120b via Ollama Cloud[/]",
        title="[bold #06B6D4]◆ CONNECTSAT MISSION CONTROL AI[/]",
        border_style="#06B6D4"
    ))


def show_response(text: str):
    """Renderiza resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M:%S")
    console.print(Panel(
        text,
        title="[bold #06B6D4]◆ ARIA — Mission Control AI[/]",
        subtitle=f"[dim]{now}[/]",
        border_style="#06B6D4",
        padding=(1, 2)
    ))


def show_help():
    """Exibe tabela de comandos disponíveis."""
    table = Table(border_style="#06B6D4", show_header=True, header_style="bold #A855F7")
    table.add_column("Comando", style="cyan")
    table.add_column("Descrição")

    table.add_row("/status", "Exibe telemetria atual e alertas ativos")
    table.add_row("/about",  "Informações sobre o ConnectSat-1 e a missão")
    table.add_row("/clear",  "Limpa o terminal")
    table.add_row("/help",   "Exibe esta tabela de comandos")
    table.add_row("/exit",   "Encerra o sistema")
    table.add_row("[dim]qualquer texto[/]", "Envia pergunta para análise da IA")

    console.print(Panel(table, title="[bold]Comandos disponíveis[/]", border_style="#06B6D4"))


def show_about():
    """Exibe informações sobre a missão ConnectSat."""
    console.print(Panel(
        "[bold]Satélite:[/] ConnectSat-1\n"
        "[bold]Órbita:[/] LEO 550km · Período orbital ~95 minutos\n"
        "[bold]Missão:[/] Conectividade rural — internet onde a fibra não chega\n"
        "[bold]Cobertura:[/] Regiões rurais do Brasil, foco Norte e Nordeste\n"
        "[bold]IA:[/] ARIA (Autonomous Response and Intelligence Analyst)\n"
        "[bold]Modelo:[/] gpt-oss:120b via Ollama Cloud\n\n"
        "[dim]Cada análise conecta dados técnicos ao impacto nas\n"
        "comunidades rurais que dependem deste satélite.[/]",
        title="[bold #A855F7]◆ Sobre o ConnectSat-1[/]",
        border_style="#A855F7"
    ))


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    if not engine.is_ready():
        console.print(
            "⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="yellow"
        )

    while True:
        try:
            user_input = session.prompt("\n❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando Mission Control AI...[/]")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("[dim]Encerrando Mission Control AI...[/]")
            break

        elif user_input == "/help":
            show_help()

        elif user_input == "/status":
            console.print("[dim]Coletando telemetria...[/]")
            show_response(engine.status_snapshot())

        elif user_input == "/about":
            show_about()

        elif user_input == "/clear":
            console.clear()
            show_banner()

        else:
            # Qualquer outra entrada vai para o motor de análise com IA
            console.print("[dim]Consultando ARIA...[/]")
            resposta = engine.analyze(user_input)
            show_response(resposta)