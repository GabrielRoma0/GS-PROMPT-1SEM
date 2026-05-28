# src/telemetria.py
# Simulação de telemetria do satélite ConnectSat (LEO - Telecomunicações)
# Parâmetros baseados em satélites estilo Starlink/OneWeb

import random
from datetime import datetime


# Faixas normais de operação de cada parâmetro
FAIXAS_NORMAIS = {
    "latencia_uplink":   (20.0,  60.0),   # milissegundos
    "throughput_feixe":  (80.0,  150.0),  # Mbps
    "saude_antena":      (85.0,  100.0),  # percentual
    "beam_steering":     (0.0,   2.0),    # graus de desvio
    "temp_transponder":  (30.0,  65.0),   # graus Celsius
}


def coletar() -> dict:
    """
    Simula uma leitura de telemetria do satélite ConnectSat.
    Retorna um dicionário com os valores atuais de cada parâmetro.
    Na maior parte do tempo os valores ficam dentro da faixa normal,
    mas há 20% de chance de cada parâmetro gerar um valor anômalo.
    """

    def valor_com_anomalia(normal_min, normal_max, limite_absoluto_max=None, fator_anomalia=1.5):
        """Gera valor normal 80% do tempo, anômalo 20% do tempo."""
        if random.random() < 0.20:  # 20% de chance de anomalia
            if random.random() < 0.5:
                valor = round(random.uniform(normal_max, normal_max * fator_anomalia), 2)
                # Respeita limite absoluto se definido
                if limite_absoluto_max:
                    valor = min(valor, limite_absoluto_max)
                return valor
            else:
                return round(random.uniform(normal_min * 0.3, normal_min), 2)
        return round(random.uniform(normal_min, normal_max), 2)

    dados = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "satelite": "ConnectSat-1",
        "orbita": "LEO 550km",
        "latencia_uplink":  valor_com_anomalia(20.0, 60.0),
        "throughput_feixe": valor_com_anomalia(80.0, 150.0),
        "saude_antena":     valor_com_anomalia(85.0, 100.0, limite_absoluto_max=100.0),
        "beam_steering":    valor_com_anomalia(0.0, 2.0),
        "temp_transponder": valor_com_anomalia(30.0, 65.0),
    }

    return dados


def formatar(dados: dict) -> str:
    """
    Formata os dados de telemetria em texto legível para o terminal.
    Usado pelo engine para montar o contexto que vai para a IA.
    """
    return f"""
📡 TELEMETRIA — {dados['satelite']} ({dados['orbita']})
🕐 Timestamp: {dados['timestamp']}

- Latência Uplink:     {dados['latencia_uplink']} ms
- Throughput do Feixe: {dados['throughput_feixe']} Mbps
- Saúde da Antena:     {dados['saude_antena']}%
- Beam Steering:       {dados['beam_steering']}°
- Temp. Transponder:   {dados['temp_transponder']}°C
""".strip()