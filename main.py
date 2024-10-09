from flask import Flask, render_template
import requests
import os  # Para lidar com as variáveis de ambiente
from bs4 import BeautifulSoup

app = Flask(__name__)

# Função para interagir com a API do Browserless
def scrape_kworb():
    # URL da API do Browserless (substitua pela sua chave de API)
    browserless_url = 'https://chrome.browserless.io/content?token=9883aff7-00df-4cef-a4e2-e583303a1975'

    # Payload simplificado para a chamada da API
    payload = {
        "url": "https://kworb.net/youtube/"
    }

    # Fazer a requisição POST para a API do Browserless
    response = requests.post(browserless_url, json=payload)

    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        return response.text
    else:
        print(f"Erro ao acessar Browserless: {response.status_code}, Detalhes: {response.text}")
        return None

@app.route('/')
def index():
    content = scrape_kworb()
    
    if content:
        # Processar o conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Localizar a tabela de artistas
        table = soup.find('table')
        
        if table:
            rows = table.find_all('tr')[1:11]  # Pegar os 10 primeiros (ignorando o cabeçalho)

            artists_data = []

            for row in rows:
                cols = row.find_all('td')
                rank = cols[0].text.strip()
                artist = cols[1].text.strip()
                views = cols[2].text.strip()
                change = cols[3].text.strip()
                weekly_views = cols[4].text.strip()

                # Adicionar os dados à lista
                artists_data.append({
                    'rank': rank,
                    'artist': artist,  # Nome original do artista
                    'views': views,
                    'change': change,
                    'weekly_views': weekly_views
                })

            return render_template('index.html', artists=artists_data)
        else:
            print("Erro: Tabela não encontrada no conteúdo recebido.")
            return "Erro: Tabela de dados não encontrada no conteúdo."

    else:
        return "Erro ao carregar os dados."

if __name__ == '__main__':
    app.run)
