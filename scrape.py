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
    """Converte formatos como '1 hour 2 minutes' para minutos inteiros"""
    if not runtime_text:
        return None

    # Padronização do texto
    text = runtime_text.lower().replace('hours', 'hour').replace('minutes', 'minute')
    
    # Regex para capturar horas e minutos separadamente
    time_pattern = r'''
        (?:(\d+)\s*hour[s]?)?    # Captura horas (ex: 1 hour)
        (?:\s*(\d+)\s*minute[s]?)?  # Captura minutos (ex: 23 minutes)
    '''
    
    match = re.search(time_pattern, text, re.VERBOSE)
    
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes
    
    # Fallback para outros formatos (ex: "1h30m")
    numbers = [int(n) for n in re.findall(r'\d+', text)]
    if len(numbers) == 2:  # Hora e minuto
        return numbers[0] * 60 + numbers[1]
    elif numbers:  # Apenas minutos ou horas
        return numbers[0] * 60 if 'hour' in text else numbers[0]
    
    return None

def map_classificacao_imdb(imdb_rating):
    """Mapeamento com limpeza mais rigorosa"""
    mapeamento = {
        'TVY7': '10',
        'TVPG': '10',
        'TV14': '14',  # Caso do exemplo
        'TVMA': '18',
        '16': '16',
        '18': '18'
    }
    
    # Limpeza agressiva de caracteres especiais e espaços
    rating_clean = re.sub(r'[^A-Z0-9]', '', imdb_rating.upper().replace('-', ''))
    
    return mapeamento.get(rating_clean, 'L')

def get_episode_rating(soup):
    """Extrai classificação indicativa das duas localizações possíveis"""
    try:
        # Primeiro método: span na seção de storyline
        rating_span = soup.find('span', class_='ipc-metadata-list-item__list-content-item', 
                              string=re.compile(r'TV-[\dA-Z]+'))
        if rating_span:
            raw_rating = rating_span.get_text(strip=True)
            logger.info(f"Classificação encontrada (span): {raw_rating}")
            return map_classificacao_imdb(raw_rating)

        # Segundo método: anchor na seção hero
        rating_anchor = soup.find('a', href=re.compile(r'parentalguide'), 
                             string=re.compile(r'TV-[\dA-Z]+'))
        if rating_anchor:
            raw_rating = rating_anchor.get_text(strip=True)
            logger.info(f"Classificação encontrada (anchor): {raw_rating}")
            return map_classificacao_imdb(raw_rating)

        # Fallback para conteúdo próximo
        parental_section = soup.find('a', href=re.compile(r'parentalguide'))
        if parental_section:
            nearby_text = parental_section.find_next(text=re.compile(r'TV-[\dA-Z]+'))
            if nearby_text:
                return map_classificacao_imdb(nearby_text.strip())

        logger.warning("Classificação não encontrada nas localizações conhecidas")
        return 'L'
        
    except Exception as e:
        logger.error(f"Erro na extração da classificação: {str(e)}")
        return 'L'

def get_episode_runtime(episode_url):
    try:
        response = requests.get(episode_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Busca na seção de Technical Specs
        runtime_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})

        if runtime_element:
            raw_text = ' '.join(runtime_element.stripped_strings)
            return parse_runtime(raw_text.split('Runtime')[-1].strip()), soup  # Remove o label
        
        return None, soup
        
    except Exception as e:
        logger.error(f"Erro ao obter runtime: {str(e)}")
        return None, soup

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
            return [], soup
            
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
                        episode_url = f"https://www.imdb.com{href.split('?')[0]}"
                        break

                if not episode_url:
                    logger.warning("Link do episódio não encontrado, pulando episódio.")
                    continue
                
                # Obtém a duração e classificação na página individual do episódio
                runtime, parsed = get_episode_runtime(episode_url)
                rating = get_episode_rating(parsed)

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
        
        return sorted(episodes, key=lambda x: x['num_episodio']), soup
        
    except Exception as e:
        logger.error(f"Erro ao obter episódios da temporada {season_number}: {str(e)}")
        return [], soup

def sql_escape(texto):
    """Sanitiza texto para uso seguro em queries SQL, removendo aspas simples e caracteres não permitidos"""
    caracteres_problematicos = {
        "'": "",   # Remove aspas simples
        "\"": "",  # Remove aspas duplas
        "\\": "",  # Remove backslashes
        "\x00": "",# Remove caractere nulo
        "\x1a": "",# Remove caractere de substituição
        ";": ""    # Remove ponto-e-vírgula (prevenção básica contra injection)
    }

    for char, substituto in caracteres_problematicos.items():
        texto = texto.replace(char, substituto)

    # Remove caracteres não-ASCII (opcional)
    texto = texto.encode('ascii', 'ignore').decode('ascii')

    return texto.strip()


def get_pais_origem(serie_id):
    """Extrai o país de origem da série"""
    try:
        url = f"https://www.imdb.com/title/{serie_id}/?ref_=ttep_ov"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra o elemento que contém "Country of origin"
        label = soup.find('span',
                         class_='ipc-metadata-list-item__label',
                         string=lambda text: text and 'Country of origin' in text)

        if not label:
            return 'N/A', soup

        # Navega para o elemento pai e pega o conteúdo seguinte
        container = label.find_parent('li', class_='ipc-metadata-list__item')
        if container:
            # Pega todos os países listados
            paises = container.find_all('a', class_='ipc-metadata-list-item__list-content-item')
            return ', '.join([p.get_text(strip=True) for p in paises]), soup

        return 'N/A', soup

    except Exception as e:
        print(f"Erro ao buscar país: {str(e)}")
        return 'N/A', soup

def get_serie_synopsis(soup):
    try:
        # Passo 1: Encontre o container principal pela classe única
        main_container = soup.find('section', class_='sc-70a366cc-4')

        # Passo 2: Dentro dele, busque o parágrafo com data-testid
        plot_paragraph = main_container.find('p', {'data-testid': 'plot'})

        # Passo 3: Pegue o span com data-testid="plot-xl"
        synopsis_tag = plot_paragraph.find('span', {'data-testid': 'plot-xl'})

        return synopsis_tag.get_text(strip=True)

    except AttributeError:
        # Fallback para estrutura alternativa (ex: seção Storyline)
        storyline_section = soup.find('div', class_='ipc-html-content-inner-div')
        if storyline_section:
            return storyline_section.get_text(strip=True).split('—')[0]

        return 'Sinopse não disponível'

def get_generos_serie(soup):
    """Extrai gêneros mesmo sem encontrar a seção Storyline"""
    try:
        # Método 1: Busca direta por links de gêneros
        generos = soup.find_all('a', href=lambda x: x and '/search/title/?genres=' in x)
        if generos:
            return list(set([g.get_text(strip=True) for g in generos]))

        # Método 2: Busca por chips de gêneros
        generos_chips = soup.find_all('span', class_='ipc-chip__text')
        if generos_chips:
            return list(set([chip.get_text(strip=True) for chip in generos_chips]))

        return []

    except Exception as e:
        logger.error(f"Erro definitivo na extração: {str(e)}")
        return []

def normalize_genres(imdb_genres_scraped, serie_nome):
    allowed_genres = ['action', 
                      'comedy',
                      'drama',
                      'sci-fi',
                      'romance',
                      'thriller',
                      'horror']

    mapped_genres = [g.strip().lower() for g in imdb_genres_scraped if g.strip().lower() in allowed_genres]

    # Garantir que a série tenha pelo menos um gênero
    if not mapped_genres:
        mapped_genres = ['action']  # default 

    # Gera SQL para os gêneros (evita duplicatas com set)
    insert_values = ",\n".join(f"('{serie_nome}', '{genre}')" for genre in set(mapped_genres))

    return insert_values
    
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
    
    output_file = f"../scripts_insercao_gerados/{serie_nome}_episodes.sql" 
    
    
    with open(output_file, 'w', encoding='utf-8') as file:

        season = 1
        while True:
            logger.info(f"Processando temporada {season}...")
            episodes, main_soup = get_season_episodes(serie_id, season)
            if not episodes:
                logger.info(f"⚠️ Temporada {season} não encontrada ou sem dados. Finalizando...")
                break
            
            logger.info(f"✓ Temporada {season}: {len(episodes)} episódios encontrados")
            
            # Extrair dados sobre a série e tratá-los para o SQL:
            if season < 2:
                synopsis = sql_escape(get_serie_synopsis(main_soup))
                pais_de_origem, soup_title = get_pais_origem(serie_id)
                if soup_title:
                    generos_serie = get_generos_serie(soup_title)
            
            if generos_serie:    
                insert_values_genres = normalize_genres(generos_serie, serie_nome)
                logger.info(f"{generos_serie}")
                
                # Gera SQL para a série
                file.write(f"""
-- Arquivo de inserção de uma série e seus episódios gerado pelo script IMDb2SQLinsertion

-- Serie: {serie_nome}

INSERT INTO Serie (nome, sinopse, pais_id)
VALUES ('{serie_nome}', '{synopsis}', (SELECT id FROM Pais WHERE nome = '{pais_de_origem}'));

                           -- Gêneros normalizados
INSERT INTO SerieGenero (serie_nome, genero)
VALUES {insert_values_genres};
""")


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
VALUES ('{serie_nome}', {season}, {ep['num_episodio']}, '{sql_escape(ep['nome'])}', {ep['duracao'] or 'NULL'}, '{ep['data_estreia'] or 'NULL'}', '{ep['classificacao']}');
""")

            season += 1
            sleep(3)

if __name__ == "__main__":
    main()

