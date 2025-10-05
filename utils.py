# utils.py
from gpt4all import GPT4All
import os
import threading


# Inicializa o modelo
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")


# --- Funções que analisam os investimentos separadamente ---

def analisar_risco(investimentos):
    prompt = "Analise o risco dos seguintes investimentos:\n"
    for i in investimentos:
        prompt += f"{i.nome}: Valor pago R${i.valor_pago:.2f}, Cotação atual R${i.cotacao_atual:.2f}\n"
    return model.generate(prompt)


def analisar_lucro_prejuizo(investimentos):
    prompt = "Analise o lucro ou prejuízo dos seguintes investimentos:\n"
    for i in investimentos:
        prompt += f"{i.nome}: Lucro/Prejuízo R${i.lucro_prejuizo:.2f}\n"
    return model.generate(prompt)


def analisar_diversificacao(investimentos):
    prompt = "Analise a diversificação da carteira:\n"
    for i in investimentos:
        prompt += f"{i.nome}\n"
    return model.generate(prompt)


def sugerir_compras_vendas(investimentos):
    prompt = "Sugira possíveis compras ou vendas com base nos investimentos:\n"
    for i in investimentos:
        prompt += f"{i.nome}: Cotação atual R${i.cotacao_atual:.2f}\n"
    return model.generate(prompt)


def alertas_importantes(investimentos):
    prompt = "Liste alertas importantes para esses investimentos:\n"
    for i in investimentos:
        prompt += f"{i.nome}: Lucro/Prejuízo R${i.lucro_prejuizo:.2f}\n"
    return model.generate(prompt)


def dicas_melhoria(investimentos):
    prompt = "Dê dicas de melhoria na carteira:\n"
    for i in investimentos:
        prompt += f"{i.nome}\n"
    return model.generate(prompt)


def oportunidades(investimentos):
    prompt = "Identifique oportunidades de investimento:\n"
    for i in investimentos:
        prompt += f"{i.nome}\n"
    return model.generate(prompt)


def monitoramento(investimentos):
    prompt = "Sugira estratégias de monitoramento para os investimentos:\n"
    for i in investimentos:
        prompt += f"{i.nome}\n"
    return model.generate(prompt)


def motivacao(investimentos):
    prompt = "Crie mensagens de incentivo para o investidor:\n"
    for i in investimentos:
        prompt += f"{i.nome}\n"
    return model.generate(prompt)


def resumo_geral(investimentos):
    prompt = "Faça um resumo geral dos investimentos:\n"
    for i in investimentos:
        prompt += f"{i.nome}: Valor pago R${i.valor_pago:.2f}, Cotação atual R${i.cotacao_atual:.2f}, Lucro/Prejuízo R${i.lucro_prejuizo:.2f}\n"
    return model.generate(prompt)


# --- Função principal que chama as 10 análises ---
def gerar_relatorio_llm(investimentos):
    if not investimentos:
        return "Nenhum investimento cadastrado."

    relatorio = ""
    relatorio += "1. Risco:\n" + analisar_risco(investimentos) + "\n\n"
    relatorio += "2. Lucro/Prejuízo:\n" + analisar_lucro_prejuizo(investimentos) + "\n\n"
    relatorio += "3. Diversificação:\n" + analisar_diversificacao(investimentos) + "\n\n"
    relatorio += "4. Compras/Vendas:\n" + sugerir_compras_vendas(investimentos) + "\n\n"
    relatorio += "5. Alertas:\n" + alertas_importantes(investimentos) + "\n\n"
    relatorio += "6. Dicas de melhoria:\n" + dicas_melhoria(investimentos) + "\n\n"
    relatorio += "7. Oportunidades:\n" + oportunidades(investimentos) + "\n\n"
    relatorio += "8. Monitoramento:\n" + monitoramento(investimentos) + "\n\n"
    relatorio += "9. Motivação:\n" + motivacao(investimentos) + "\n\n"
    relatorio += "10. Resumo geral:\n" + resumo_geral(investimentos)

    return relatorio
