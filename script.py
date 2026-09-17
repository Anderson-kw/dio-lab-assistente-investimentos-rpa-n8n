import requests
from bs4 import BeautifulSoup

URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# 1) Baixar a página
html = requests.get(URL_PAGINA).text

# 2) Ler a tabela de clientes
soup = BeautifulSoup(html, "html.parser")
linhas = soup.select("#clientes tbody tr")

clientes = []

for linha in linhas:
    colunas = linha.find_all("td")

    cliente = {
        "nome":  colunas[0].get_text(strip=True),
        "email": colunas[1].get_text(strip=True),
        "saldo": colunas[2].get_text(strip=True),
        "perfil": colunas[3].get_text(strip=True),
    }

    clientes.append(cliente)

print(f"Total de clientes extraídos: {len(clientes)}")

# 3) Enviar para o Webhook do n8n
N8N_WEBHOOK = "http://localhost:5678/webhook-test/Clientes"

response = requests.post(N8N_WEBHOOK, json={"clientes": clientes})

print(f"Status do envio para o n8n: {response.status_code}")