from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os  # Adicione esta linha para importar a biblioteca os

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://kworb.net/youtube/'
    response = requests.get(url)
    
    # Garantir que a codificação da resposta seja 'utf-8'
    response.encoding = 'utf-8'
    
    # Processar o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Localizar a tabela de artistas
    table = soup.find('table')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))  # Esta linha agora está correta




