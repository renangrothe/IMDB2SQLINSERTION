#!/bin/bash

# Lista de séries populares
SERIES_NAMES=(
  "Stranger Things"
  "Breaking Bad"
  "Game of Thrones"
  "The Office"
  "The Mandalorian"
  "Friends"
  "The Witcher"
  "The Crown"
  "Black Mirror"
  "Sherlock"
  "Narcos"
  "Dark"
  "Peaky Blinders"
  "The Walking Dead"
  "Chernobyl"
  "Dexter"
  "The Big Bang Theory"
  "How I Met Your Mother"
  "Rick and Morty"
  "Lucifer"
  "The 100"
  "The Umbrella Academy"
  "The Boys"
  "Fleabag"
)

SERIES_IDS=(
  "tt4574334"
  "tt0903747"
  "tt0944947"
  "tt0386676"
  "tt8111088"
  "tt0108778"
  "tt5180504"
  "tt4786824"
  "tt2085059"
  "tt1475582"
  "tt2707408"
  "tt5753856"
  "tt2442560"
  "tt1520211"
  "tt7366338"
  "tt0773262"
  "tt0898266"
  "tt0460649"
  "tt2861424"
  "tt4052886"
  "tt2661044"
  "tt1312171"
  "tt1190634"
  "tt5687612"
)

# Caminho para o diretório onde o script scrape.py está localizado
SCRIPT_DIR="/home/renan/Documents/Code/python/experiments/webscraper-imdb"

# Itera sobre cada série na lista
for i in "${!SERIES_NAMES[@]}"; do
    NAME="${SERIES_NAMES[$i]}"
    ID="${SERIES_IDS[$i]}"
    # Executa o script scrape.py para cada série
    python "$SCRIPT_DIR/scrape.py" "$ID" "$NAME"
done
