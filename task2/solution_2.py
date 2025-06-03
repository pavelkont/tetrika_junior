import requests
from bs4 import BeautifulSoup
import csv
import time
import re

BASE_URL = "https://ru.wikipedia.org"
START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

RUSSIAN_LETTER_RE = re.compile(r"[А-ЯЁ]")

def get_russian_alphabet():
    alphabet = [chr(code) for code in range(ord('А'), ord('Я') + 1)]
    insert_index = alphabet.index('Е') + 1
    alphabet.insert(insert_index, 'Ё')
    return alphabet

RUSSIAN_ALPHABET_ORDER = {char: i for i, char in enumerate(get_russian_alphabet())}

def russian_letter_sort_key(letter):
    return RUSSIAN_ALPHABET_ORDER.get(letter, float('inf'))

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return None

def collect_counts():
    result = {}
    next_url = START_URL

    while next_url:
        soup = get_soup(next_url)
        if not soup:
            break

        items = soup.select("div.mw-category li")
        for item in items:
            title = item.get_text()
            if title:
                first_letter = title[0].upper()
                if RUSSIAN_LETTER_RE.fullmatch(first_letter):
                    result[first_letter] = result.get(first_letter, 0) + 1

        next_link = soup.find("a", string="Следующая страница")
        if next_link and next_link.get("href"):
            next_url = BASE_URL + next_link["href"]
            time.sleep(0.5)
        else:
            next_url = None

    return result

def write_to_csv(data, filename="beasts.csv"):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for letter in sorted(data.keys(), key=russian_letter_sort_key):
                writer.writerow([letter, data[letter]])
        print(f"\n✅ Результаты сохранены в файл {filename}.")
    except IOError as e:
        print(f"Ошибка при записи в файл {filename}: {e}")

if __name__ == "__main__":
    counts = collect_counts()
    if counts:
        write_to_csv(counts)
    else:
        print("Не удалось собрать данные.")
