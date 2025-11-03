import pytest

import test_data 

from books import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def fill_collector(collector):
        
    for name_book, genre_book in test_data.books.items():
        collector.add_new_book(name_book)
        collector.set_book_genre(name_book, genre_book)

    collector.add_new_book("Без жанра")

    return collector