import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import re
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.imdb.com/'
}

def sql_escape(text):
    """Previne SQL injection e formatação incorreta"""
    return text.replace("'", "") if text else 'NULL'
   

def clean_title(title):
    """Remove o prefixo S1.E1 e limpa o título"""
    cleaned = re.sub(r'S\d+\.E\d+\s*∙\s*', '', title)
    cleaned = cleaned.strip()
    #cleaned = cleaned.replace("'", "''")
    return cleaned

def parse_airdate(raw_date):
    """Converte datas com melhor precisão"""
    if not raw_date:
        return None

    # Normalização de meses em português
    month_map = {
        'jan': 'Jan', 'fev': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
        'mai': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
        'set': 'Sep', 'out': 'Oct', 'nov': 'Nov', 'dez': 'Dec'
    }

    cleaned_date = re.sub(r'[.]|(\s+de\s+)', ' ', raw_date.strip(), flags=re.IGNORECASE)
    for pt, en in month_map.items():
        cleaned_date = cleaned_date.replace(pt, en)

    date_formats = [
        '%d %b %Y', '%b %d %Y', '%Y-%m-%d',
        '%d %B %Y', '%B %d %Y', '%d/%m/%Y'
    ]

    for fmt in date_formats:
        try:
            dt = datetime.strptime(cleaned_date, fmt)
            return dt.strftime('%Y-%m-%d')
        except:
            continue

    # Fallback para extração de ano
    year_match = re.search(r'\b(19|20)\d{2}\b', cleaned_date)
    return f"{year_match.group(0)}-01-01" if year_match else None

def parse_runtime(runtime_text):
    """Converte texto de duração para o padrão 'XXmin'"""
    if not runtime_text:
        return None
    runtime_text = runtime_text.strip()
    minutes_match = re.search(r'(\d+)\s*min', runtime_text, re.IGNORECASE)
    if minutes_match:
        return f"{minutes_match.group(1)}"
    hours_match = re.search(r'(\d+)h\s*(\d+)m', runtime_text, re.IGNORECASE)
    if hours_match:
        total_minutes = int(hours_match.group(1)) * 60 + int(hours_match.group(2))
        return f"{total_minutes}min"
    return runtime_text if runtime_text != 'N/A' else None

def map_classificacao_imdb(imdb_rating):
    """Converte as classificações do IMDb para o padrão especificado"""
    mapeamento = {
        'L': 'L',
        'TV-Y': 'L',
        'TV-G': 'L',
        'TV-PG': '10',
        'TV-Y7': '10',
        'TV-14': '14',
        'TV-MA': '18',
        '16': '16',  # Caso apareça direto
        '18': '18'    # Caso apareça direto
    }
    
    # Extrai apenas números ou siglas conhecidas
    rating_clean = re.sub(r'[^A-Z0-9]', '', imdb_rating.upper())
    
    return mapeamento.get(rating_clean, 'L')  # Default para 'L' se não encontrar

def get_episode_rating(soup):
    """Extrai e converte a classificação indicativa"""
    try:
        # Encontra o elemento de duração primeiro
        runtime_li = soup.find('li', string=re.compile(r'\d+\s*min', re.IGNORECASE))
        
        if runtime_li:
            rating_li = runtime_li.find_previous_sibling('li')
            if rating_li:
                rating_element = rating_li.find('a', href=re.compile(r'parentalguide'))
                if rating_element:
                    raw_rating = rating_element.text.strip()
                    return map_classificacao_imdb(raw_rating)
                
                # Fallback para texto direto
                raw_rating = rating_li.get_text(strip=True)
                return map_classificacao_imdb(raw_rating)
        
        # Fallback alternativo
        cert_element = soup.find('a', href=re.compile(r'parentalguide'))
        if cert_element:
            return map_classificacao_imdb(cert_element.text.strip())
        
    except Exception as e:
        logger.error(f"Erro na classificação: {str(e)}")
    
    return 'L'  

def get_episode_runtime(episode_url):
    """Extrai duração e classificação indicativa"""
    try:
        response = requests.get(episode_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrai duração como número inteiro
        runtime_element = soup.find('li', string=re.compile(r'\d+\s*(min|h)', re.IGNORECASE))
        runtime = parse_runtime(runtime_element.text) if runtime_element else None

        # Extrai classificação
        rating = get_episode_rating(soup)

        return runtime, rating

    except Exception as e:
        logger.error(f"Erro ao obter dados do episódio: {str(e)}")
        return 'N/A', 'L'

def get_season_episodes(serie_id, season_number):
    try:
        url = f"https://www.imdb.com/title/{serie_id}/episodes?season={season_number}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        episodes = []
        
        # Tenta encontrar os itens de episódio com data-testid; se não encontrar, usa o fallback.
        episode_items = soup.find_all('div', attrs={'data-testid': 'episodes-browse-episode'})
        if episode_items:
            logger.info(f"Encontrados {len(episode_items)} episódios usando o seletor 'episodes-browse-episode'.")
        else:
            logger.info("Não encontrou 'episodes-browse-episode', buscando 'article.episode-item-wrapper'.")
            episode_items = soup.find_all('article', class_='episode-item-wrapper')
            logger.info(f"Encontrados {len(episode_items)} episódios usando o fallback 'episode-item-wrapper'.")
        
        if not episode_items:
            return []
            
        for item in episode_items:
            try:
                # Extrai título e número do episódio
                title_element = item.find('h4')
                if not title_element:
                    title_element = item.find('a', class_='ipc-link')
                if not title_element:
                    continue
                    
                full_title = title_element.text.strip()
                ep_num_match = re.search(r'S\d+\.E(\d+)', full_title)
                if not ep_num_match:
                    continue
                ep_num = int(ep_num_match.group(1))
                title = clean_title(full_title)
                
                # Extrai a data de estreia (airdate)
                airdate = None
                airdate_element = item.find('span', class_={'sc-f2169d65-10', 'bYaARM'})
                if not airdate_element:
                    airdate_element = item.find('span', class_='air-date')
                if airdate_element:
                    airdate = parse_airdate(airdate_element.text)
                
                # Extrai o link do episódio a partir dos candidatos
                link_candidates = item.find_all('a', class_='ipc-lockup-overlay ipc-focusable')
                episode_url = None
                for candidate in link_candidates:
                    href = candidate.get('href', '')
                    if '/title/tt' in href and 'ref_' in href:
                        # Usa a versão em português (/pt/) conforme informado
                        episode_url = f"https://www.imdb.com/pt{href.split('?')[0]}"
                        break
                if not episode_url:
                    logger.warning("Link do episódio não encontrado, pulando episódio.")
                    continue
                
                # Obtém a duração na página individual do episódio
                runtime, rating = get_episode_runtime(episode_url)

                episodes.append({
                    'num_episodio': ep_num,
                    'nome': title,
                    'data_estreia': airdate or '1900-01-01',
                    'duracao': runtime,
                    'classificacao': rating
                }) 
                
            except Exception as ep_error:
                logger.error(f"Erro ao processar episódio: {str(ep_error)}")
                continue
        
        return sorted(episodes, key=lambda x: x['num_episodio'])
        
    except Exception as e:
        logger.error(f"Erro ao obter episódios da temporada {season_number}: {str(e)}")
        return []

def main():
    """Função principal agora recebe parâmetros"""
    
    # Caso queira rodar o script fora de um shell environment, insira os dados da série aqui
    # serie_id = 
    # serie_nome = 

    if len(sys.argv) == 3:
        serie_id = sys.argv[1]
        serie_nome = sys.argv[2]
        logger.info(f"Iniciando scraping para: {serie_nome} ({serie_id})")
    else:
        serie_id = input("ID da série (ex: tt0903747): ").strip()
        serie_nome = input("Nome da série (ex: Breaking Bad): ").strip()
    
    output_file = f"{serie_nome}_episodes.sql" 

    with open(output_file, 'w', encoding='utf-8') as file:
        season = 1
        while True:
            logger.info(f"Processando temporada {season}...")
            episodes = get_season_episodes(serie_id, season)
            if not episodes:
                logger.info(f"⚠️ Temporada {season} não encontrada ou sem dados. Finalizando...")
                break
            
            logger.info(f"✓ Temporada {season}: {len(episodes)} episódios encontrados")
            
            # Determina o ano da temporada baseado na data de estreia do primeiro episódio
            season_year = episodes[0]['data_estreia'][:4] if episodes[0]['data_estreia'] != '1900-01-01' else None
            if not season_year:
                for ep in episodes:
                    year_match = re.search(r'\d{4}', str(ep))
                    if year_match:
                        season_year = year_match.group(0)
                        break
            if not season_year:
                season_year = '1900'
            
            # Gera SQL para a temporada e seus episódios
            file.write(f"""
-- Temporada {season} ({season_year})
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('{serie_nome}', {season}, {season_year}, {len(episodes)});
""")
            
            for ep in episodes:
                file.write(f"""
INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('{serie_nome}', {season}, {ep['num_episodio']}, '{sql_escape(ep['nome'])}', '{ep['duracao'] or 'NULL'}', '{ep['data_estreia'] or 'NULL'}', '{ep['classificacao']}');
""")

            season += 1
            sleep(3)

if __name__ == "__main__":
    main()

