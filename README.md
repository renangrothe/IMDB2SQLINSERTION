 # 🎬 IMDb Episode Scraper  
  
 Este projeto é um scraper desenvolvido em Python que coleta informações de episódios de uma série no [IMDb](https://www.imdb.com), acessando diretamente a página de cada episódio. O script gera um arquivo SQL contendo comandos de inserção para popular um banco de dados com os dados extraídos.  
  
 ## 🚀 Funcionalidades  
  
 Extrai informações de todas as temporadas disponíveis de uma série.  
  
 Para cada episódio, coleta:  
  
 - **Nome do episódio**  
 - **Número do episódio**  
 - **Data de estreia**  
 - **Duração** (em minutos, sem o sufixo "min")  
 - **Classificação indicativa** (mapeada para o padrão brasileiro: L, 10, 12, 14, 16, 18)  
  
 Salva os dados estruturados em um arquivo SQL pronto para inserção no banco de dados.  
  
 **Input dinâmico**: Recebe o ID da série e o nome via linha de comando ou input interativo.  
  
 ---  
  
 ## 🛠️ Pré-requisitos  
  
 Antes de executar o script, instale as dependências necessárias:  
  
 ```bash  
 pip install requests beautifulsoup4  
 ```  
  
 ---  
  
 ## 📜 Como Usar  
  
 ### 1. Obtenha o ID da série  
  
 - Acesse a página da série no [IMDb](https://www.imdb.com).  
 - Navegue até a seção **"Guia de Episódios"** (exemplo: *Stranger Things - Guia de Episódios*).  
 - O **ID da série** é o código na URL:  
  
   **Exemplo**: `tt4574334` para *Stranger Things*.  
  
 ### 2. Execute o script  
  
 #### Modo automático (via linha de comando):  
  
 ```bash  
 python scrape.py tt4574334 "Stranger Things"  
 ```  
  
 #### Modo interativo:  
  
 ```bash  
 python scrape.py  
 ```  
  
 O script solicitará o **ID** e o **nome da série**.  
  
 ### 3. Resultado  
  
 Um arquivo SQL será gerado com o nome `{serie_id}_episodes.sql`.  
  
 **Exemplo de saída:**  
  
 ```sql  
 -- Temporada 1 (2016)  
 INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)  
 VALUES ('Stranger Things', 1, 2016, 8);  
  
 INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)  
 VALUES ('Stranger Things', 1, 1, 'Chapter One: The Vanishing of Will Byers', 47, '2016-07-15', '14');  
 ```  
  
 ---  
  
 ## 🏗️ Estrutura do Projeto  
  
 ```plaintext  
 📂 imdb_scraper/  
  ├── scrape.py             # Script principal  
  ├── {serie_id}_episodes.sql # Arquivo SQL gerado  
  ├── README.md              # Documentação  
 ```  

 ---  
  
 ## 🛑 Notas Importantes  
  
 - O IMDb pode bloquear requisições frequentes. O script já inclui **delays** (`time.sleep()`) entre as requisições.  
 - A estrutura do IMDb pode mudar, exigindo ajustes nos **seletores CSS** usados no `BeautifulSoup`.  
 - Para integração com o projeto **[Sistema de Avaliação de Séries](https://github.com/renangrothe/Sistema-De-Avaliacao-de-Series)**, certifique-se de que o banco de dados esteja configurado corretamente.  
  
 ---  
  
 ## 📄 Licença  
  
 Este projeto é de código aberto e pode ser utilizado livremente.  
  
 ---  
  
 ## 🔗 Referências  
  
 - [IMDb](https://www.imdb.com)  
 - [Sistema de Avaliação de Séries](https://github.com/renangrothe/Sistema-De-Avaliacao-de-Series)  

