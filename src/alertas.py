# src/alertas.py
# Regras de threshold e lógica de decisão do ConnectSat
# A IA explica — o Python decide.

# Thresholds por parâmetro
# Cada parâmetro tem nível ATENCAO e CRITICO
THRESHOLDS = {
    "latencia_uplink": {
        "atencao":  60.0,   # ms — começa a degradar experiência do usuário
        "critico":  120.0,  # ms — inaceitável para telemedicina e videoaula
    },
    "throughput_feixe": {
        "atencao":  80.0,   # Mbps — abaixo disso afeta múltiplos usuários
        "critico":  40.0,   # Mbps — serviço praticamente inutilizável
    },
    "saude_antena": {
        "atencao":  85.0,   # % — degradação detectável
        "critico":  70.0,   # % — risco de perda de cobertura
    },
    "beam_steering": {
        "atencao":  2.0,    # graus — início de perda de alinhamento
        "critico":  4.0,    # graus — perda severa de sinal
    },
    "temp_transponder": {
        "atencao":  65.0,   # °C — limite operacional normal
        "critico":  80.0,   # °C — risco de dano permanente ao hardware
    },
}

# Impacto terrestre de cada parâmetro — conecta técnico com social
IMPACTO_TERRESTRE = {
    "latencia_uplink": "aulas online e teleconsultas médicas em comunidades rurais",
    "throughput_feixe": "velocidade de internet de escolas e postos de saúde conectados",
    "saude_antena": "cobertura de sinal para toda a área de serviço do feixe",
    "beam_steering": "qualidade de conexão de todos os usuários no feixe ativo",
    "temp_transponder": "integridade do hardware — falha pode tirar o satélite de operação",
}


def avaliar(dados: dict) -> list:
    """
    Avalia os dados de telemetria e retorna lista de alertas.
    Cada alerta é um dicionário com: parametro, valor, nivel, mensagem, impacto.
    Retorna lista vazia se tudo estiver normal.
    """
    alertas = []

    # --- Latência Uplink (quanto MAIOR, pior) ---
    lat = dados["latencia_uplink"]
    if lat >= THRESHOLDS["latencia_uplink"]["critico"]:
        alertas.append({
            "parametro": "Latência Uplink",
            "valor": f"{lat} ms",
            "nivel": "CRÍTICO",
            "mensagem": f"Latência de {lat}ms está acima do limite crítico de 120ms.",
            "impacto": IMPACTO_TERRESTRE["latencia_uplink"],
            "acao_automatica": "Iniciando roteamento alternativo pelo feixe de backup.",
        })
    elif lat >= THRESHOLDS["latencia_uplink"]["atencao"]:
        alertas.append({
            "parametro": "Latência Uplink",
            "valor": f"{lat} ms",
            "nivel": "ATENÇÃO",
            "mensagem": f"Latência de {lat}ms acima do ideal (60ms).",
            "impacto": IMPACTO_TERRESTRE["latencia_uplink"],
            "acao_automatica": None,
        })

    # --- Throughput do Feixe (quanto MENOR, pior) ---
    thr = dados["throughput_feixe"]
    if thr <= THRESHOLDS["throughput_feixe"]["critico"]:
        alertas.append({
            "parametro": "Throughput do Feixe",
            "valor": f"{thr} Mbps",
            "nivel": "CRÍTICO",
            "mensagem": f"Throughput de {thr}Mbps abaixo do limite crítico de 40Mbps.",
            "impacto": IMPACTO_TERRESTRE["throughput_feixe"],
            "acao_automatica": "Ativando compressão de dados e priorizando tráfego essencial.",
        })
    elif thr <= THRESHOLDS["throughput_feixe"]["atencao"]:
        alertas.append({
            "parametro": "Throughput do Feixe",
            "valor": f"{thr} Mbps",
            "nivel": "ATENÇÃO",
            "mensagem": f"Throughput de {thr}Mbps abaixo do recomendado (80Mbps).",
            "impacto": IMPACTO_TERRESTRE["throughput_feixe"],
            "acao_automatica": None,
        })

    # --- Saúde da Antena (quanto MENOR, pior) ---
    ant = dados["saude_antena"]
    if ant <= THRESHOLDS["saude_antena"]["critico"]:
        alertas.append({
            "parametro": "Saúde da Antena",
            "valor": f"{ant}%",
            "nivel": "CRÍTICO",
            "mensagem": f"Saúde da antena em {ant}% — abaixo do limite crítico de 70%.",
            "impacto": IMPACTO_TERRESTRE["saude_antena"],
            "acao_automatica": "Ativando elementos redundantes da antena phased-array.",
        })
    elif ant <= THRESHOLDS["saude_antena"]["atencao"]:
        alertas.append({
            "parametro": "Saúde da Antena",
            "valor": f"{ant}%",
            "nivel": "ATENÇÃO",
            "mensagem": f"Saúde da antena em {ant}% — monitoramento reforçado.",
            "impacto": IMPACTO_TERRESTRE["saude_antena"],
            "acao_automatica": None,
        })

    # --- Beam Steering (quanto MAIOR, pior) ---
    beam = dados["beam_steering"]
    if beam >= THRESHOLDS["beam_steering"]["critico"]:
        alertas.append({
            "parametro": "Beam Steering",
            "valor": f"{beam}°",
            "nivel": "CRÍTICO",
            "mensagem": f"Desvio de {beam}° no apontamento — acima do limite crítico de 4°.",
            "impacto": IMPACTO_TERRESTRE["beam_steering"],
            "acao_automatica": "Executando recalibração automática de apontamento.",
        })
    elif beam >= THRESHOLDS["beam_steering"]["atencao"]:
        alertas.append({
            "parametro": "Beam Steering",
            "valor": f"{beam}°",
            "nivel": "ATENÇÃO",
            "mensagem": f"Desvio de {beam}° no apontamento — monitorando estabilidade.",
            "impacto": IMPACTO_TERRESTRE["beam_steering"],
            "acao_automatica": None,
        })

    # --- Temperatura do Transponder (quanto MAIOR, pior) ---
    temp = dados["temp_transponder"]
    if temp >= THRESHOLDS["temp_transponder"]["critico"]:
        alertas.append({
            "parametro": "Temperatura do Transponder",
            "valor": f"{temp}°C",
            "nivel": "CRÍTICO",
            "mensagem": f"Temperatura de {temp}°C acima do limite crítico de 80°C.",
            "impacto": IMPACTO_TERRESTRE["temp_transponder"],
            "acao_automatica": "Ativando modo de resfriamento e reduzindo carga do transponder.",
        })
    elif temp >= THRESHOLDS["temp_transponder"]["atencao"]:
        alertas.append({
            "parametro": "Temperatura do Transponder",
            "valor": f"{temp}°C",
            "nivel": "ATENÇÃO",
            "mensagem": f"Temperatura de {temp}°C aproximando-se do limite (80°C).",
            "impacto": IMPACTO_TERRESTRE["temp_transponder"],
            "acao_automatica": None,
        })

    return alertas


def resumo(alertas: list) -> str:
    """Retorna texto resumido dos alertas para injetar no prompt da IA."""
    if not alertas:
        return "✅ Todos os parâmetros dentro dos limites normais de operação."

    linhas = []
    for a in alertas:
        emoji = "🔴" if a["nivel"] == "CRÍTICO" else "🟡"
        linhas.append(f"{emoji} [{a['nivel']}] {a['parametro']}: {a['mensagem']}")
        linhas.append(f"   Impacto terrestre: {a['impacto']}")
        if a["acao_automatica"]:
            linhas.append(f"   ⚡ Ação automática: {a['acao_automatica']}")

    return "\n".join(linhas)