# 🎬 IMDb Episode Scraper

Este projeto é um **scraper** desenvolvido em Python que coleta informações de episódios de uma série no IMDb, acessando diretamente a página de cada episódio. O script gera um arquivo SQL contendo comandos de inserção para popular um banco de dados com os dados extraídos.

## 🚀 Funcionalidades
- Extrai informações de todas as temporadas disponíveis de uma série.
- Para cada episódio, coleta:
  - Nome do episódio
  - Número do episódio
  - Data de estreia
  - Duração
  - Nota IMDb (opcional)
- Salva os dados estruturados em um arquivo **SQL** pronto para inserção no banco de dados.

## 🛠️ Pré-requisitos
Antes de executar o script, instale as dependências necessárias:

```sh
pip install requests beautifulsoup4
```

## 📜 Como Usar
1. **Defina o ID da série** no IMDb. Exemplo: `tt4574334` para *Stranger Things*.
2. **Execute o script**:

```sh
python crawler.py
```

3. O script **baixará os dados** e gerará um arquivo `inserts_corrigido.sql` com os comandos SQL de inserção.

## 🏗️ Estrutura do Projeto
```
📂 imdb_scraper/
 ├── crawler.py            # Script principal
 ├── inserts_corrigido.sql  # Arquivo SQL gerado
 ├── README.md             # Documentação
```

## ⚙️ Configuração e Personalização
Se desejar alterar a série extraída, edite a variável **serie_id** no arquivo `crawler.py`:

```python
serie_id = 'tt4574334'  # ID da série desejada
```

Caso queira alterar a **versão do IMDb**, ajuste a URL para `/pt/` (português) ou `/en/` (inglês):

```python
episode_url = f"https://www.imdb.com/pt{href.split('?')[0]}"
```

## 🔍 Exemplo de Output
Após a execução, o arquivo `inserts_corrigido.sql` conterá comandos como:

```sql
-- Temporada 1 (2016)
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('Stranger Things', 1, 2016, 8);

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia)
VALUES ('Stranger Things', 1, 1, 'Chapter One: The Vanishing of Will Byers', '47min', '2016-07-15');
```

## 🛑 Notas Importantes
- O IMDb pode bloquear requisições frequentes. Caso ocorra, adicione **delays** (`time.sleep()`) entre as requisições.
- A estrutura do IMDb pode mudar, exigindo ajustes nos seletores CSS usados no BeautifulSoup.

## 📄 Licença
Este projeto é de código aberto e pode ser utilizado livremente.


