# src/engine.py
# Motor de análise da Mission Control AI — ConnectSat
# Integra telemetria + alertas + IA generativa (Ollama Cloud)

import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

from src.telemetria import coletar, formatar
from src.alertas import avaliar, resumo

load_dotenv()

# Identificação da trilha
TRILHA = "connectsat"

# Cliente Ollama Cloud
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)


def load_system_prompt() -> str:
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de controle de missão espacial."


def llm(prompt: str, system: str = None, max_tokens: int = 800, temperature: float = 0.3) -> str:
    """
    Envia prompt ao gpt-oss:120b via Ollama Cloud e retorna a resposta.
    Ponto único de contato com a IA — toda chamada passa por aqui.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        # Coleta stream em partes e monta a resposta completa
        resposta_completa = ""
        for part in client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=True
        ):
            resposta_completa += part['message']['content']
        return resposta_completa.strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


class MissionEngine:
    """
    Motor principal da Mission Control AI.
    Coordena telemetria, alertas e análise por IA generativa.
    """

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        # Histórico das últimas leituras para contexto temporal
        self.historico = []

    def is_ready(self) -> bool:
        """Retorna True quando o engine está implementado e funcional."""
        return True

    def status_snapshot(self) -> str:
        """
        Coleta telemetria atual e retorna resumo do estado da missão.
        Usado pelo comando /status na CLI.
        """
        dados = coletar()
        alertas = avaliar(dados)

        # Guarda no histórico (mantém últimas 5 leituras)
        self.historico.append(dados)
        if len(self.historico) > 5:
            self.historico.pop(0)

        telemetria_formatada = formatar(dados)
        resumo_alertas = resumo(alertas)

        status = f"{telemetria_formatada}\n\n"

        if alertas:
            status += f"⚠️  ALERTAS DETECTADOS:\n{resumo_alertas}"
        else:
            status += "✅ Todos os parâmetros dentro dos limites normais."

        return status

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Análise completa: coleta dados, avalia alertas, monta prompt e consulta IA.
        Este é o método central — chamado para cada mensagem do usuário na CLI.
        """
        # 1. Coleta telemetria atual
        dados = coletar()
        alertas = avaliar(dados)

        # Guarda no histórico
        self.historico.append(dados)
        if len(self.historico) > 5:
            self.historico.pop(0)

        # 2. Monta contexto do histórico (memória temporal)
        contexto_historico = ""
        if len(self.historico) > 1:
            contexto_historico = "\n📊 HISTÓRICO DAS ÚLTIMAS LEITURAS:\n"
            for i, h in enumerate(self.historico[:-1], 1):
                contexto_historico += (
                    f"Leitura -{len(self.historico) - i}: "
                    f"latência={h['latencia_uplink']}ms, "
                    f"throughput={h['throughput_feixe']}Mbps, "
                    f"temp={h['temp_transponder']}°C\n"
                )

        # 3. Monta o prompt com dados reais injetados
        resumo_alertas = resumo(alertas)
        telemetria_formatada = formatar(dados)

        prompt = f"""
{telemetria_formatada}

{contexto_historico}

🚨 ALERTAS ATIVOS:
{resumo_alertas}

❓ PERGUNTA DO OPERADOR:
{pergunta_usuario}

Analise a situação acima e responda ao operador seguindo sua estrutura obrigatória.
Cite os valores numéricos reais da telemetria na sua resposta.
Conecte sempre a análise técnica ao impacto nas comunidades rurais atendidas.
""".strip()

        # 4. Consulta a IA com system prompt + prompt montado
        return llm(prompt, system=self.system_prompt)