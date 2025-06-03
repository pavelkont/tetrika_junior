import pytest
from solution_2 import get_russian_alphabet, russian_letter_sort_key, collect_counts

def test_alphabet_order():
    alphabet = get_russian_alphabet()
    assert 'Ё' in alphabet
    assert alphabet.index('Ё') == alphabet.index('Е') + 1

    shuffled = ['Б', 'Д', 'Ё', 'Е', 'Ж', 'А']
    sorted_letters = sorted(shuffled, key=russian_letter_sort_key)
    assert sorted_letters == ['А', 'Б', 'Д', 'Е', 'Ё', 'Ж']

def test_collect_counts_letters_only_russian(monkeypatch):
    from solution_2 import get_soup

    class MockTag:
        def __init__(self, text):
            self.text = text
        def get_text(self):
            return self.text

    def mock_get_soup(_):
        class Dummy:
            def select(self, _):
                return [MockTag("Акула"), MockTag("Ёж"), MockTag("123"), MockTag("Zebra")]
            def find(self, *_, **__):
                return None
        return Dummy()

    monkeypatch.setattr("solution_2.get_soup", mock_get_soup)
    counts = collect_counts()
    assert counts == {"А": 1, "Ё": 1}
