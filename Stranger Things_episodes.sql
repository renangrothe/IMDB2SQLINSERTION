
-- Serie: Stranger Things
INSERT INTO Serie (nome, sinopse, (SELECT id FROM Pais WHERE nome = 'pais_de_origem')
VALUES ('Stranger Things', 'sinopse_dummy', 'pais_dummy');

-- Temporada 1 (2016)
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('Stranger Things', 1, 2016, 8);

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 1, 'Chapter One: The Vanishing of Will Byers', 47, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 2, 'Chapter Two: The Weirdo on Maple Street', 55, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 3, 'Chapter Three: Holly, Jolly', 51, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 4, 'Chapter Four: The Body', 49, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 5, 'Chapter Five: The Flea and the Acrobat', 52, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 6, 'Chapter Six: The Monster', 46, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 7, 'Chapter Seven: The Bathtub', 41, '2016-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 1, 8, 'Chapter Eight: The Upside Down', 54, '2016-01-01', '14');

-- Temporada 2 (2017)
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('Stranger Things', 2, 2017, 9);

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 1, 'Chapter One: MADMAX', 48, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 2, 'Chapter Two: Trick or Treat, Freak', 56, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 3, 'Chapter Three: The Pollywog', 51, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 4, 'Chapter Four: Will the Wise', 46, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 5, 'Chapter Five: Dig Dug', 58, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 6, 'Chapter Six: The Spy', 51, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 7, 'Chapter Seven: The Lost Sister', 45, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 8, 'Chapter Eight: The Mind Flayer', 47, '2017-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 2, 9, 'Chapter Nine: The Gate', 62, '2017-01-01', '14');

-- Temporada 3 (2019)
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('Stranger Things', 3, 2019, 8);

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 1, 'Chapter One: Suzie, Do You Copy?', 50, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 2, 'Chapter Two: The Mall Rats', 50, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 3, 'Chapter Three: The Case of the Missing Lifeguard', 49, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 4, 'Chapter Four: The Sauna Test', 52, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 5, 'Chapter Five: The Flayed', 51, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 6, 'Chapter Six: E Pluribus Unum', 59, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 7, 'Chapter Seven: The Bite', 55, '2019-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 3, 8, 'Chapter Eight: The Battle of Starcourt', 76, '2019-01-01', '14');

-- Temporada 4 (2022)
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('Stranger Things', 4, 2022, 9);

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 1, 'Chapter One: The Hellfire Club', 78, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 2, 'Chapter Two: Vecnas Curse', 77, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 3, 'Chapter Three: The Monster and the Superhero', 63, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 4, 'Chapter Four: Dear Billy', 78, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 5, 'Chapter Five: The Nina Project', 76, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 6, 'Chapter Six: The Dive', 75, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 7, 'Chapter Seven: The Massacre at Hawkins Lab', 98, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 8, 'Chapter Eight: Papa', 85, '2022-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 4, 9, 'Chapter Nine: The Piggyback', 139, '2022-01-01', '14');

-- Temporada 5 (2025)
INSERT INTO Temporada (serie_nome, num_temporada, ano_lancamento, num_episodios)
VALUES ('Stranger Things', 5, 2025, 8);

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 1, 'Chapter One: The Crawl', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 2, 'Chapter Two: The Vanishing of', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 3, 'Chapter Three: The Turnbow Trap', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 4, 'Chapter Four: Sorcerer', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 5, 'Chapter Five: Shock Jock', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 6, 'Chapter Six: Escape from Camazotz', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 7, 'Chapter Seven: The Bridge', NULL, '2025-01-01', '14');

INSERT INTO Episodio (serie_nome, num_temporada, num_episodio, nome, duracao, data_estreia, classificacao)
VALUES ('Stranger Things', 5, 8, 'Chapter Eight: The Rightside Up', NULL, '2025-01-01', '14');
