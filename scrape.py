import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import re
import logging

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

def clean_title(title):
    """Remove o prefixo S1.E1 e limpa o título"""
    cleaned = re.sub(r'S\d+\.E\d+\s*∙\s*', '', title)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("'", "''")
    return cleaned

def parse_airdate(raw_date):
    """Converte datas do IMDB para formato SQL"""
    if not raw_date:
        return None
    cleaned_date = raw_date.strip().replace('.', '')
    date_formats = [
        '%d %b %Y',  # ex: 15 Jul 2016
        '%b %d, %Y', # ex: Jul 15, 2016
        '%Y-%m-%d',  # ex: 2016-07-15
        '%B %d, %Y'  # ex: July 15, 2016
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(cleaned_date, fmt).strftime('%Y-%m-%d')
        except Exception:
            continue
    year_match = re.search(r'\d{4}', cleaned_date)
    if year_match:
        return f"{year_match.group(0)}-01-01"
    return None

def parse_runtime(runtime_text):
    """Converte texto de duração para o padrão 'XXmin'"""
    if not runtime_text:
        return None
    runtime_text = runtime_text.strip()
    minutes_match = re.search(r'(\d+)\s*min', runtime_text, re.IGNORECASE)
    if minutes_match:
        return f"{minutes_match.group(1)}min"
    hours_match = re.search(r'(\d+)h\s*(\d+)m', runtime_text, re.IGNORECASE)
    if hours_match:
        total_minutes = int(hours_match.group(1)) * 60 + int(hours_match.group(2))
        return f"{total_minutes}min"
    return runtime_text if runtime_text != 'N/A' else None

def get_episode_runtime(episode_url):
    """Extrai a duração do episódio a partir da sua página individual usando busca por regex no texto do <li>"""
    if not episode_url:
        return "N/A"
    try:
        logger.info(f"Obtendo duração para o episódio: {episode_url}")
        response = requests.get(episode_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Busca diretamente um <li> cujo texto contenha o padrão 'XX min'
        runtime_element = soup.find('li', text=re.compile(r'\d+\s*min', re.IGNORECASE))
        if runtime_element:
            runtime_text = runtime_element.text.strip()
            parsed_runtime = parse_runtime(runtime_text)
            logger.info(f"Duração extraída: '{parsed_runtime}' a partir do texto '{runtime_text}'")
            return parsed_runtime
        else:
            logger.warning(f"Nenhum elemento contendo 'min' foi encontrado na página: {episode_url}")
    except Exception as e:
        logger.error(f"Erro ao obter duração do episódio {episode_url}: {str(e)}")
    return "N/A"

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
                runtime = get_episode_runtime(episode_url)
                
                episodes.append({
                    'num_episodio': ep_num,
                    'nome': title,
                    'data_estreia': airdate or '1900-01-01',
                    'duracao': runtime or 'N/A'
                })
                
            except Exception as ep_error:
                logger.error(f"Erro ao processar episódio: {str(ep_error)}")
                continue
        
        return sorted(episodes, key=lambda x: x['num_episodio'])
        
    except Exception as e:
        logger.error(f"Erro ao obter episódios da temporada {season_number}: {str(e)}")
        return []

def main():
    serie_id = 'tt4574334'  # Stranger Things
    serie_nome = 'Stranger Things'
    output_file = 'inserts_corrigido.sql'
    
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
INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia)
VALUES ('{serie_nome}', {season}, {ep['num_episodio']}, '{ep['nome']}', '{ep['duracao']}', '{ep['data_estreia']}');
""")
            
            season += 1
            sleep(3)

if __name__ == "__main__":
    main()

