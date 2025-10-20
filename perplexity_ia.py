import os
import requests
from models import User, Investimento
from app import *

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "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")

def get_ativos_dict():
    """
    Retorna uma lista de dicionários com os dados dos investimentos.
    """
    with app.app_context():
        return [
            {c.name: getattr(inv, c.name) for c in inv.__table__.columns}
            for inv in Investimento.query.all()
        ]

def gerar_relatorio_ia(prompt: str,
                      model: str = "sonar-pro",
                      max_tokens: int = 800,
                      temperature: float = 0.5) -> str:
    """
    Chama a API da Perplexity AI para gerar um relatório com base no prompt.
    Retorna o texto da resposta.
    """
    if not PERPLEXITY_API_KEY:
        raise ValueError("Chave de API da Perplexity não configurada (PERPLEXITY_API_KEY)")

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Analise e sugira investimentos"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        error_text = getattr(e.response, 'text', '')
        raise RuntimeError(f"Erro ao chamar API Perplexity: {e} - {error_text}")
    except (KeyError, IndexError):
        raise RuntimeError(f"Resposta inesperada da API Perplexity: {response.text}")

def format_ativo(inv) -> str:
    """
    Formata os dados de um ativo para o prompt.
    """
    ticker = inv.get("ticker") if isinstance(inv, dict) else getattr(inv, "ticker", "")
    nome = inv.get("nome") if isinstance(inv, dict) else getattr(inv, "nome", "")
    quantidade = inv.get("quantidade") if isinstance(inv, dict) else getattr(inv, "quantidade", 0)
    valor_pago = inv.get("valor_pago") if isinstance(inv, dict) else getattr(inv, "valor_pago", 0.0)
    cotacao_atual = inv.get("cotacao_atual") if isinstance(inv, dict) else getattr(inv, "cotacao_atual", 0.0)
    return f"- Ticker: {ticker}, Nome: {nome}, Quantidade: {quantidade}, Valor pago: {valor_pago:.2f}, Cotação atual: {cotacao_atual:.2f}"

def gerar_relatorio_carteira(ativos: list, usuario: str) -> str:
    """
    Monta um prompt específico para relatório da carteira do usuário
    e chama gerar_relatorio_ia().
    """
    prompt = f"Relatório de investimentos para o usuário {usuario}.\nAtivos:\n"
    prompt += "\n".join([format_ativo(inv) for inv in ativos])
    prompt += (
        "\n\nAnalise os ativos, calcule lucro/prejuízo, identifique pontos de atenção e sugira próximas ações.\n"
    )
    return gerar_relatorio_ia(prompt)
