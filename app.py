from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Função para fazer scraping diretamente do site Kworb
def scrape_kworb():
    # URL do Kworb
    kworb_url = 'https://kworb.net/youtube/'

    # Fazer a requisição GET para o site do Kworb
    response = requests.get(kworb_url)

    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        return response.text
    else:
        print(f"Erro ao acessar Kworb: {response.status_code}, Detalhes: {response.text}")
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
                if len(cols) < 5:
                    continue  # Certificar que a linha tem todas as colunas esperadas

                rank = cols[0].text.strip()
                artist = cols[1].text.strip()
                views = cols[2].text.strip()
                change = cols[3].text.strip()
                weekly_views = cols[4].text.strip()

                # Encontrar o link do vídeo (se presente)
                link_tag = row.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    video_link = link_tag['href']
                    
                    # Ajustar o link do vídeo corretamente
                    if video_link.startswith('video/'):
                        video_id = video_link.replace('video/', '').replace('.html', '')
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                    else:
                        video_url = video_link  # Caso a URL já seja completa

                    # Adicionar os dados à lista
                    artists_data.append({
                        'rank': rank,
                        'artist': artist,
                        'views': views,
                        'change': change,
                        'weekly_views': weekly_views,
                        'video_url': video_url  # Incluindo o link para o vídeo
                    })

            return render_template('index.html', artists=artists_data)
        else:
            print("Erro: Tabela não encontrada no conteúdo recebido.")
            return "Erro: Tabela de dados não encontrada."

    else:
        return "Erro ao carregar os dados."

if __name__ == '__main__':
    app.run()
